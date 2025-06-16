from multiprocessing import shared_memory
import json
import time,functools

SHM_SIZE = 4096  # bytes
SYNC_TAG = 0xCAFEBABE
MAX_STALE_SECONDS = 1.0
MAX_FRAME_REPEAT = 5

def guarded_access(role: str):
    def decorator(func):
        last_frame = {"frame": None, "count": 0}

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)

            if not isinstance(result, dict):
                print(f"[Guard:{role}] Unexpected result type from {func.__name__}")
                return result

            tag = result.get("SyncTag")
            if tag != SYNC_TAG:
                #print(f"[Guard:{role}] SyncTag mismatch: expected {SYNC_TAG:x}, got {tag}")
                return {}

            frame = result.get("Frame")
            #if frame is not None:
            #    if frame == last_frame["frame"]:
            #        last_frame["count"] += 1
            #        if last_frame["count"] > MAX_FRAME_REPEAT:
            #            print(f"[Guard:{role}] Frame {frame} repeated {last_frame['count']} times — possible stall")
            #    else:
            #        last_frame["frame"] = frame
            #        last_frame["count"] = 0

            timestamp = result.get("Timestamp")
            if timestamp:
                age = time.time() - timestamp
                if age > MAX_STALE_SECONDS:
                    print(f"[Guard:{role}] Frame age {age:.2f}s — stale data?")

            return result

        return wrapper
    return decorator


class Achsmemory:
    def __init__(self, name, create=False, wait=False):
        self.name = name
        self.frame_id = 0
        if create:
            try:
                self.shm = shared_memory.SharedMemory(name=name, create=True, size=SHM_SIZE)
                self._init_empty()
            except FileExistsError:
                shared_memory.SharedMemory(name=name).unlink()
                self.shm = shared_memory.SharedMemory(name=name, create=True, size=SHM_SIZE)
                self._init_empty()
        elif wait:
            self.shm = self.wait_for_shared_memory(name)
        else:
            self.shm = shared_memory.SharedMemory(name=name)

    def wait_for_shared_memory(self, name, timeout=5):
        start = time.time()
        while time.time() - start < timeout:
            try:
                return shared_memory.SharedMemory(name=name)
            except FileNotFoundError:
                time.sleep(0.1)
        raise TimeoutError(f"Shared memory segment {name} not found after {timeout} seconds")

    def _init_empty(self):
        template = {
            "active": 0,
            "frames": [
                {"SyncTag": SYNC_TAG, "Frame": 0},
                {"SyncTag": SYNC_TAG, "Frame": 1},
            ]
        }
        self._write_dict(template)

    def _raw_read(self) -> dict:
        raw_bytes = bytes(self.shm.buf).split(b'\0', 1)[0]
        if not raw_bytes:
            return {"active": 0, "frames": [{}, {}]}
        try:
            return json.loads(raw_bytes.decode("utf-8"))
        except json.JSONDecodeError:
            print("[Achsmemory] Warning: JSON parse error in shared memory")
            return {"active": 0, "frames": [{}, {}]}

    def _raw_write(self, payload: bytes):
        if not isinstance(payload, bytes):
            raise TypeError("[_raw_write] Expected bytes, got", type(payload))
        if len(payload) > SHM_SIZE:
            raise ValueError(f"[raw_write] Payload size {len(payload)} exceeds SHM_SIZE={SHM_SIZE}")
        self.shm.buf[:len(payload)] = payload
        self.shm.buf[len(payload):] = b'\0' * (SHM_SIZE - len(payload))

    def _write_dict(self, data: dict):
        payload = json.dumps(data).encode("utf-8")
        self._raw_write(payload)

    # ---------------- Frame Write Methods ----------------

    def write(self, data: dict):
        raw = self._raw_read()
        active = raw.get("active", 0)
        next_frame = 1 - active
        frame_data = {
            "SyncTag": SYNC_TAG,
            "Frame": raw["frames"][active].get("Frame", 0) + 1,
            **data
        }
        raw["frames"][next_frame] = frame_data
        raw["active"] = next_frame
        self._write_dict(raw)

    # ---------------- Pending / Confirmed Methods ----------------

    def write_pending(self, data: dict):
        payload = json.dumps({"pending": data}).encode("utf-8")
        if len(payload) > SHM_SIZE:
            raise ValueError(f"Payload too large: {len(payload)} > {SHM_SIZE}")
        #print(f"[DEBUG] Pending payload length: {len(payload)}")
        self._raw_write(payload)

    @guarded_access("backend-read")
    def read_pending(self) -> dict:
        return self._raw_read().get("pending", {})


    def _mark_confirmed(self):
        pass

    def write_confirmed(self, data: dict):
        payload = json.dumps({"confirmed": data}).encode("utf-8")
        if len(payload) > SHM_SIZE:
            raise ValueError(f"Payload too large: {len(payload)} > {SHM_SIZE}")
        #print(f"[DEBUG] Final payload length: {len(payload)}")
        self._raw_write(payload)


    @guarded_access("controller-read")
    def read_confirmed(self) -> dict:
        return self._raw_read().get("confirmed", {})

    def read(self) -> dict:
        raw = self._raw_read()
        active = raw.get("active", 0)
        frame = raw["frames"][active]
        if frame.get("SyncTag") != SYNC_TAG:
            print("[Achsmemory] Warning: SyncTag mismatch — possible corruption.")
            return {}
        return frame

    def close(self):
        self.shm.close()

    def unlink(self):
        self.shm.unlink()
