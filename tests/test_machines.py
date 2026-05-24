import os
import sys
import unittest

# tm_engine.py dosyasını içe aktarabilmek için ana dizini yola ekliyoruz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from tm_engine import TuringMachine
except ImportError:
    print("Hata: tm_engine.py dosyası ana dizinde bulunamadı!")
    sys.exit(1)

class TestTuringMachines(unittest.TestCase):

    def run_machine(self, yaml_filename, input_str):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'machines'))
        yaml_path = os.path.join(base_dir, yaml_filename)
        
        if yaml_filename == "student_choice.yaml" and not os.path.exists(yaml_path):
            yaml_path = os.path.join(base_dir, "divisible_by_4.yaml")

        if not os.path.exists(yaml_path):
            self.skipTest(f"{yaml_filename} dosyası bulunamadığı için test atlandı.")

        tm = TuringMachine.from_yaml(yaml_path)
        # NOT: Eğer motorundaki fonksiyon adı farklıysa (.simulate veya .start gibi) burayı guncelle:
        result = tm.run(input_str) 
        return result

    # TM-1 Testleri
    def test_tm1_unary_to_binary(self):
        self.assertTrue(self.run_machine("unary_to_binary.yaml", "111"))
        self.assertTrue(self.run_machine("unary_to_binary.yaml", "11111"))
        self.assertFalse(self.run_machine("unary_to_binary.yaml", "0"))
        self.assertFalse(self.run_machine("unary_to_binary.yaml", "1101"))
        self.assertFalse(self.run_machine("unary_to_binary.yaml", ""))

    # TM-2 Testleri
    def test_tm2_binary_compare(self):
        self.assertTrue(self.run_machine("binary_compare.yaml", "11#10"))
        self.assertTrue(self.run_machine("binary_compare.yaml", "101#100"))
        self.assertFalse(self.run_machine("binary_compare.yaml", "10#11"))
        self.assertFalse(self.run_machine("binary_compare.yaml", "11#11"))
        self.assertFalse(self.run_machine("binary_compare.yaml", "#"))

    # TM-3 Testleri
    def test_tm3_string_copy(self):
        self.assertTrue(self.run_machine("string_copy.yaml", "abba"))
        self.assertTrue(self.run_machine("string_copy.yaml", "ab"))
        self.assertFalse(self.run_machine("string_copy.yaml", "a#b"))
        self.assertFalse(self.run_machine("string_copy.yaml", "abc"))
        self.assertTrue(self.run_machine("string_copy.yaml", ""))

    # TM-4 Testleri
    def test_tm4_divisible_by_4(self):
        self.assertTrue(self.run_machine("student_choice.yaml", "100"))
        self.assertTrue(self.run_machine("student_choice.yaml", "1100"))
        self.assertFalse(self.run_machine("student_choice.yaml", "11"))
        self.assertFalse(self.run_machine("student_choice.yaml", "101"))
        self.assertTrue(self.run_machine("student_choice.yaml", "0"))

if __name__ == '__main__':
    unittest.main()