import importlib.util
import pathlib
import sys
import types
import unittest
from unittest.mock import Mock, patch

class QueueSecurityTests(unittest.TestCase):
    def test_only_configured_admin_can_clear_queue(self):
        bot = Mock()
        bot.message_handler.side_effect = lambda **kwargs: lambda fn: fn
        config = types.ModuleType("config")
        config.token = "dummy"
        config.admin_user_ids = {7}
        telebot = types.ModuleType("telebot")
        telebot.TeleBot = Mock(return_value=bot)
        logger = types.ModuleType("loggerconfig")
        logger.getLogger = Mock(return_value=Mock())
        with patch.dict(sys.modules, {"config": config, "telebot": telebot, "loggerconfig": logger}):
            spec = importlib.util.spec_from_file_location("queue_main", pathlib.Path(__file__).parents[1]/"main.py")
            module = importlib.util.module_from_spec(spec)
            with patch("pickle.load", return_value=[]), patch("builtins.open", unittest.mock.mock_open()):
                spec.loader.exec_module(module)
        module.queue = [(1, "tester")]
        with patch.object(module, "save_data") as save:
            module.clear_queue(types.SimpleNamespace(from_user=types.SimpleNamespace(id=2, username="guest"),chat=types.SimpleNamespace(id=2)))
            self.assertEqual(len(module.queue), 1)
            save.assert_not_called()
            module.clear_queue(types.SimpleNamespace(from_user=types.SimpleNamespace(id=7, username="admin"),chat=types.SimpleNamespace(id=7)))
            self.assertEqual(module.queue, [])
            save.assert_called_once()

if __name__ == "__main__": unittest.main()
