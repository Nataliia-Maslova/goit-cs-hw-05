import argparse
import asyncio
import logging
from aiopath import AsyncPath
from aioshutil import copyfile


# Асинхронна функція для рекурсивного читання папки і копіювання файлів
async def read_folder(path: AsyncPath, output: AsyncPath) -> None:
    try:
        # Ітеруємося по всіх файлах і папках у директорії
        async for item in path.iterdir():
            if await item.is_dir():
                # Якщо це директорія, рекурсивно обробляємо її
                await read_folder(item, output)
            elif await item.is_file():
                # Якщо це файл, викликаємо функцію копіювання
                await copy_file(item, output)
    except Exception as e:
        logging.error(f"Error reading folder {path}: {e}")


# Асинхронна функція для копіювання файлу на основі його розширення
async def copy_file(file: AsyncPath, output: AsyncPath) -> None:
    try:
        extension_name = file.suffix[1:]  # Отримуємо розширення файлу (без крапки)
        extension_folder = output / extension_name
        await extension_folder.mkdir(exist_ok=True, parents=True)  # Створюємо папку, якщо її не існує
        await copyfile(file, extension_folder / file.name)  # Копіюємо файл до відповідної папки
        logging.info(f"Copied {file} to {extension_folder / file.name}")
    except Exception as e:
        logging.error(f"Error copying file {file}: {e}")


if __name__ == "__main__":
    # Налаштовуємо логування
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    # Створюємо парсер аргументів командного рядка
    parser = argparse.ArgumentParser(description="Async file sorter by extension.")
    parser.add_argument("source", type=str, help="Path to the source folder")
    parser.add_argument("output", type=str, help="Path to the output folder")
    args = parser.parse_args()

    # Ініціалізуємо шляхи до вихідної та цільової директорій
    source = AsyncPath(args.source)
    output = AsyncPath(args.output)

    # Запускаємо асинхронну обробку файлів
    asyncio.run(read_folder(source, output))

    # Для перевірки на відповідність стандартам PEP8 можна використати:
    # pycodestyle --show-source --show-pep8 <назва_файлу>.py
