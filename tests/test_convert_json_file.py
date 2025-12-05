import sys
import tempfile
import json
import os
# ensure project root is on sys.path for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from toon_app import convert_json_file, flatten_to_toon


def test_convert_json_file_basic():
    data = {"name": "UnitTest", "vals": [1, 2, 3]}
    # create a temp json file
    tf = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json", encoding="utf-8")
    json.dump(data, tf)
    tf.flush()
    tf.close()
    try:
        result_path, status, preview = convert_json_file(tf.name)
        assert result_path is not None, f"Expected result file, got {result_path}, status: {status}"
        assert "Succès" in status
        # preview should match flatten_to_toon
        expected = flatten_to_toon(data)
        assert preview == expected
        assert os.path.exists(result_path)
        with open(result_path, 'r', encoding='utf-8') as f:
            content = f.read()
        assert content == expected
    finally:
        # cleanup
        try:
            os.remove(tf.name)
        except Exception:
            pass
        try:
            if result_path and os.path.exists(result_path):
                os.remove(result_path)
        except Exception:
            pass


if __name__ == '__main__':
    test_convert_json_file_basic()
    print('test passed')
