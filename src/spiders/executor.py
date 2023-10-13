from settings import Config
from logger import error_log
import execjs


class JSExecutor:

    def __init__(self):
        ...

    def __call__(self, code_path: str, function: str, args: list):
        try:
            with open(code_path, "r") as file:
                js_code = file.read()
            ctx = execjs.compile(js_code)
            return ctx.call(function, *args)
        except (FileNotFoundError, Exception) as e:
            error_log.error(f'execute js code fail: {e=}')


if __name__ == '__main__':
    secret_code = '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'
    js_executor = JSExecutor()

    res = js_executor(
        code_path=Config.ZZZMH_DECRYPT_PATH,
        function='zzzmh_decrypt',
        args=[secret_code]
    )
    print(res)
