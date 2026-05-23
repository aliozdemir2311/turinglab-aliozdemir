import yaml
from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class Configuration:
    state: str
    tape: str
    head_position: int

@dataclass
class RunResult:
    accepted: bool
    final_tape: str
    steps: int
    history: List[Configuration] = field(default_factory=list)
    reason: str = ""

class TuringMachine:
    def __init__(self, config: Dict[str, Any]):
        self.name = config.get("name", "Unnamed")
        self.states = config.get("states", [])
        self.input_alphabet = config.get("input_alphabet", [])
        self.tape_alphabet = config.get("tape_alphabet", [])
        self.blank = config.get("blank", "B")
        self.start_state = config.get("start_state", "")
        self.accept_states = config.get("accept_states", [])
        self.reject_states = config.get("reject_states", [])
        
        # Geçiş kurallarını (transitions) hızlı arama için sözlüğe çeviriyoruz
        self.transitions = {}
        for t in config.get("transitions", []):
            self.transitions[(t["state"], t["read"])] = t

    def run(self, input_string: str, max_steps: int = 1000, verbose: bool = False) -> RunResult:
        # Şeridi sözlük olarak başlatıyoruz (negatif indeksleri kolay yönetmek için)
        tape: Dict[int, str] = {}
        for i, char in enumerate(input_string):
            tape[i] = char
        
        head_pos = 0
        current_state = self.start_state
        history = []
        
        def get_tape_str(tape_dict, head_pos):
            if not tape_dict:
                return f"[{self.blank}]"
            min_idx = min(min(tape_dict.keys()), head_pos)
            max_idx = max(max(tape_dict.keys()), head_pos)
            
            result = ""
            for i in range(min_idx, max_idx + 1):
                char = tape_dict.get(i, self.blank)
                if i == head_pos:
                    result += f"[{char}]"
                else:
                    result += char
            return result

        for step in range(max_steps + 1):
            tape_str_for_history = "".join([tape.get(i, self.blank) for i in range(min(tape.keys(), default=0), max(tape.keys(), default=0) + 1)])
            if not tape_str_for_history:
                tape_str_for_history = self.blank
                
            history.append(Configuration(current_state, tape_str_for_history, head_pos))
            
            current_symbol = tape.get(head_pos, self.blank)
            
            if verbose:
                print(f"Adım {step} | Durum: {current_state} | Şerit: {get_tape_str(tape, head_pos)}")

            if current_state in self.accept_states:
                return RunResult(True, tape_str_for_history, step, history, "accept")
            
            if current_state in self.reject_states:
                return RunResult(False, tape_str_for_history, step, history, "reject")

            transition_key = (current_state, current_symbol)
            if transition_key not in self.transitions:
                return RunResult(False, tape_str_for_history, step, history, "no_transition")

            rule = self.transitions[transition_key]
            tape[head_pos] = rule["write"]
            current_state = rule["next"]
            
            if rule["move"] == "R":
                head_pos += 1
            elif rule["move"] == "L":
                head_pos -= 1

        return RunResult(False, tape_str_for_history, max_steps, history, "timeout")

class SingleTapeTM:
    @staticmethod
    def from_yaml(filepath: str) -> TuringMachine:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
            return TuringMachine(config)
        except Exception as e:
            raise ValueError(f"YAML okuma hatasi: {e}")