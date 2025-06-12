from multiprocessing import shared_memory
import json,time

SHM_SIZE = 4096  # bytes

class Achsmemory:
    def __init__(self, name, create=False, wait=False):
        if create:
            try:
                self.shm = shared_memory.SharedMemory(name=name, create=True, size=SHM_SIZE)
            except FileExistsError:
                shared_memory.SharedMemory(name=name).unlink()
                self.shm = shared_memory.SharedMemory(name=name, create=True, size=SHM_SIZE)
        elif wait:
            self.shm = self.wait_for_shared_memory(name)
        else:
            self.shm = shared_memory.SharedMemory(name=name)

    def wait_for_shared_memory(self,name, timeout=5):
        start = time.time()
        while time.time() - start < timeout:
            try:
                return shared_memory.SharedMemory(name=name)
            except FileNotFoundError:
                time.sleep(0.1)
        raise TimeoutError(f"Shared memory segment {name} not found after {timeout} seconds")


    def write(self, data: dict):
        payload = json.dumps(data).encode("utf-8")
        self.shm.buf[:len(payload)] = payload
        self.shm.buf[len(payload):] = b'\0' * (SHM_SIZE - len(payload))

    def read(self) -> dict:
        raw = bytes(self.shm.buf).split(b'\0', 1)[0]
        if not raw:
            return {}
        try:
            return json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            print("[Achsmemory] Warning: Invalid JSON in shared memory")
            return {}

    def close(self):
        self.shm.close()

    def unlink(self):
        self.shm.unlink()
