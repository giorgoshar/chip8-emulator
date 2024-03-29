
class console:
    @staticmethod
    def error(message :str) -> None:
        print(f"\033[1;31m[ERROR] {message}\033[0m")
        exit(1)
    @staticmethod
    def warn(message :str) -> None:
        print(f"\033[1;33m[WARNING] {message}\033[0m")
    @staticmethod
    def info(message :str) -> None:
        print(f"\033[1;34m[INFO] {message}\033[0m")
    @staticmethod
    def done(message :str) -> None:
        print(f"\033[1;32m[DONE] {message}\033[0m")

if __name__ == "__main__":
    console.warn('Warning')
    console.info('Information')
    console.done('Done')
    console.error('Error')
