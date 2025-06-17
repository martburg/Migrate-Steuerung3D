from transitions import Machine
from enum import Enum, auto

class AxisState(str, Enum):
    OFFLINE =                "offline"
    ONLINE =                 "online"
    ONLINE_WAITING =         "online_waiting"
    TO_INIT =                "to_init"
    INIT =                   "init"
    TO_IDLE =                "to_idle"
    IDLE =                   "idle"
    MOVING =                 "moving"
    HOLDING =                "holding"
    FAULT =                  "fault"
    RECOVERING =             "recovering"
    EDIT_POS_PROPS =         "edit_PosProps"
    TO_E_POS_PROPS =         "to_e_PosProps"
    EDIT_VEL_PROPS =         "edit_VelProps"
    TO_E_VEL_PROPS =         "to_e_VelProps"
    EDIT_FILTER_PROPS =      "edit_FilterProps"
    TO_E_FILTER_PROPS =      "to_e_FilterProps"
    EDIT_GUIDE_PROPS =       "edit_GuideProps"
    TO_E_GUIDE_PROPS =       "to_e_GuideProps"
    WAITING_ESTOP_CLEAR=     "waiting_estop_clear"
    WAITING_ESTOP_ENGAGE=    "waiting_estop_engage"
    WAITING_WRITE_CONFIRM =  "waiting_write_confirm"


class AxisStateMachine:
    states = [state.value for state in AxisState]

    def __init__(self):
        
        self.machine = Machine(model=self, states=AxisStateMachine.states, initial=AxisState.OFFLINE.value)

        to_estop=[
        'online', 'online_waiting',
        'init', 'idle', 'moving',
        'edit_PosProps', 'edit_VelProps',
        'edit_FilterProps', 'edit_GuideProps']


        to_waiting_wtite_confirm = ["edit_PosProps",
                                    "edit_VelProps",
                                    "edit_FilterProps",
                                    "edit_GuideProps"]

        # More granular transitions
        self.machine.add_transition('t_online',                 'offline',                    'online',            conditions='can_online')
        self.machine.add_transition('t_offline',                '*',                          'offline')
        self.machine.add_transition("t_online_waiting",         "online",                     "online_waiting")
        self.machine.add_transition("t_to_init",                "online_waiting",             "to_init",           conditions="can_init")
        self.machine.add_transition('enter_init',               'to_init',                    'init')
        self.machine.add_transition('init_done',                'init',                       'to_idle',           conditions='is_ready')
        self.machine.add_transition('enter_idle',               'to_idle',                    'idle')
        self.machine.add_transition('start_move',               'idle',                       'moving',           conditions=['is_enabled', 'is_moving'])
        self.machine.add_transition('move',                     'holding',                    'moving',           conditions=['is_enabled', 'is_moving'])
        self.machine.add_transition('hold',                     'moving',                     'holding',          conditions='is_enabled')
        self.machine.add_transition('stop_motion',              'moving',                     'idle',             conditions=['is_disabled'])
        self.machine.add_transition('stop_motion',              'holding',                    'idle',             conditions=['is_disabled'])
        self.machine.add_transition('hold',                     'idle',                       'holding',          conditions=['is_enabled', 'is_not_moving'])

        self.machine.add_transition('trip',                     '*',                          'fault',             conditions='has_fault')
        self.machine.add_transition('recover',                  'fault',                      'recovering',        conditions='wants_reset')
        self.machine.add_transition('resume',                   'recovering',                 'idle',              conditions=['is_ready', 'no_fault'])
        self.machine.add_transition('shutdown',                 '*',                          'offline',           conditions='in_estop')
        self.machine.add_transition('t_e_PosProps',             'init',                       'to_e_PosProps',     conditions='in_init')
        self.machine.add_transition('t_edit_PosProps',          'to_e_PosProps',              'edit_PosProps')
        self.machine.add_transition('t_e_VelProps',             'init',                       'to_e_VelProps',     conditions='in_init')
        self.machine.add_transition('t_edit_VelProps',          'to_e_VelProps',              'edit_VelProps')
        self.machine.add_transition('t_e_FilterProps',          'init',                       'to_e_FilterProps',  conditions='in_init')
        self.machine.add_transition('t_edit_FilterProps',       'to_e_FilterProps',           'edit_FilterProps')
        self.machine.add_transition('t_e_GuideProps',           'init',                       'to_e_GuideProps',   conditions='in_init')
        self.machine.add_transition('t_edit_GuideProps',        'to_e_GuideProps',            'edit_GuideProps')        
        self.machine.add_transition('t_finish_edit',            'edit_PosProps',              'init')
        self.machine.add_transition('t_finish_edit',            'edit_VelProps',              'init')
        self.machine.add_transition('t_finish_edit',            'edit_FilterProps',           'init')
        self.machine.add_transition('t_finish_edit',            'edit_GuideProps',            'init')
        self.machine.add_transition('t_request_estop_clear',    'init',                       'waiting_estop_clear')
        self.machine.add_transition('t_request_estop_engage',   '*',                          'waiting_estop_engage')

        self.machine.add_transition("t_waiting_write_confirm",   to_waiting_wtite_confirm,    "waiting_write_confirm")
        self.machine.add_transition("t_confirm_write",           "waiting_write_confirm",     "init")
        self.machine.add_transition('t_request_estop_clear',     'fault',                     'waiting_estop_clear')
        self.machine.add_transition('t_back_to_init',            'waiting_estop_clear',       'init', conditions='is_ready')
        self.machine.add_transition('t_back_to_init', 'waiting_estop_engage', 'init', conditions='in_estop')


        self._actprop = {}
        self._estop = {}
        self._setprop = {}
        self._prev_state = self.state
        self._init_achse_latched = False
        self._estop_engaged_latched = False


    def update(self, actprop: dict, estop: dict, setprop: dict):
        """Update the state machine based on the latest properties."""
        self._actprop = actprop
        self._estop = estop
        self._setprop = setprop
        self._prev_state = self.state

        if getattr(self._actprop, "InitAchse", 0) == 1:
            self._init_achse_latched = True  

        try:
            # --- Axis name check ---
            axis_name = setprop.get("Name", "") if isinstance(setprop, dict) else getattr(setprop, "Name", "")
            axis_name = axis_name.strip() if axis_name else ""
            #print(f"[StateMachine] axis_name check: axis_name='{axis_name}', state='{self.state}'")

            if not axis_name:
                if self.state != AxisState.OFFLINE.value:
                    print("[StateMachine] Axis name is empty — forcing offline.")
                    self.t_offline()
                return self.state

            # --- Highest priority: Fault handling ---
            if self.has_fault():
                #print(f"[StateMachine] Fault detected: EStopStatus = {getattr(self._actprop, 'EStopStatus', 0)}")
                self.trip()
                return self.state

            # --- Handle normal transitions step-by-step ---
            if self.state == AxisState.OFFLINE.value:
                if self.can_online():
                    print("[StateMachine] Transitioning OFFLINE → ONLINE")
                    self.t_online()

            elif self.state == AxisState.ONLINE.value:
                print("[StateMachine] Transitioning ONLINE → ONLINE_WAITING")
                self.t_online_waiting()
            
            elif self.state == AxisState.ONLINE_WAITING.value:
                print(f"[StateMachine] In ONLINE_WAITING state. Checking can_init:")
                print(f" - in_estop = {self.in_estop()}")
                print(f" - InitAchse = {getattr(self._actprop, 'InitAchse', 'MISSING')}")
                print(f" - InitAchseLatched = {self._init_achse_latched}")
                if self.can_init():
                    print("[StateMachine] Transitioning ONLINE → TO_INIT")
                    self.t_to_init()
                    self._init_achse_latched = False

            elif self.state == AxisState.TO_INIT.value:
                print("[StateMachine] Transitioning TO_INIT → INIT")
                self.enter_init()

            elif self.state == AxisState.INIT.value:
                if self.in_estop():
                    #print("[StateMachine] Still in E-Stop, staying in INIT.")
                    return self.state
                print("[StateMachine] INIT done, transitioning → TO_IDLE")
                self.init_done()

            elif self.state == AxisState.TO_IDLE.value:
                print("[StateMachine] Transitioning TO_IDLE → IDLE")
                self.enter_idle()

            elif self.state == AxisState.IDLE.value:
                if self.is_enabled() and not self.is_moving():
                    print("[StateMachine] Joystick held (no motion), transitioning IDLE → HOLDING")
                    self.hold()
                elif self.is_moving():
                    print("[StateMachine] Motion detected, transitioning IDLE → MOVING")
                    self.start_move()
            elif self.state == AxisState.MOVING.value:
                if self.is_enabled():
                        print("[StateMachine] Joystick held, transitioning MOVING → HOLDING")
                        self.hold()

            elif self.state == AxisState.HOLDING.value:
                if self.is_moving():
                    print("[StateMachine] Motion resumed, transitioning HOLDING → MOVING")
                    self.move()
                elif self.is_disabled():
                    print("[StateMachine] Enable released, transitioning HOLDING → IDLE")
                    self.stop_motion()
            elif self.state == AxisState.FAULT.value:
                if self.wants_reset():
                    print("[StateMachine] Reset requested, transitioning FAULT → RECOVERING")
                    self.recover()

            elif self.state == AxisState.RECOVERING.value:
                if self.is_ready() and self.no_fault():
                    print("[StateMachine] Recover complete, transitioning RECOVERING → IDLE")
                    self.resume()
            elif self.state == AxisState.WAITING_ESTOP_CLEAR.value:
                if self.is_ready():
                    print("[StateMachine] EStop cleared — transitioning WAITING_ESTOP_CLEAR → INIT")
                    self.t_back_to_init()

            elif self.state == AxisState.WAITING_ESTOP_ENGAGE.value:
                if self.in_estop():
                        print("[StateMachine] E-Stop engaged confirmed — transitioning WAITING_ESTOP_ENGAGE → INIT")
                        self.t_back_to_init()

            # --- Emergency shutdown if estop engaged in operational states ---
            if self.in_estop() and self.state in {
                AxisState.TO_IDLE.value,
                AxisState.IDLE.value,
                AxisState.MOVING.value,
                AxisState.HOLDING.value,
                AxisState.RECOVERING.value,
                AxisState.FAULT.value
            }:
                print("[StateMachine] E-Stop detected — shutting down.")
                self.shutdown()

        except Exception as e:
            print(f"[StateMachine] Transition error: {e}")

        return self.state


    # --- Conditions ---
    def can_online(self):
        return getattr(self._setprop, "Name", "" ) != ""
    
    def has_fault(self):
        pass
        #return getattr(self._actprop, "EStopStatus", 0) != 2048  # Assuming 2048 means no fault

    def no_fault(self):
        pass
        #return getattr(self._actprop, "EStopStatus", 0) == 2048  # Assuming 2048 means no fault

    def can_init(self):
        return self.in_estop() and self._init_achse_latched
    
    def is_ready(self):
        return not self.in_estop()

    def wants_reset(self):
        return self.in_estop() and getattr(self._actprop, "EStopReset", False)

    def is_moving(self):
        return abs(getattr(self._actprop, "SpeedSoll", 0)) > 0.01
    
    def is_enabled(self):
        return getattr(self._actprop, "Enable", False)
    
    def is_disabled(self):
        return not getattr(self._actprop, "Enable", False)

    def in_estop(self):
        return not getattr(self._estop, "EsMaster", False)
    
    def is_not_moving(self):
        return not self.is_moving() 
    
    def in_init(self):
        return self.state == AxisState.INIT.value or self.state == AxisState.TO_INIT.value