import os
import shutil
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing import Pool, cpu_count

# =====================================================================
#                ЧАСТИНА 1 — СОРТУВАННЯ ФАЙЛІВ (ПОТОКИ)
# =====================================================================

def copy_file(file_path: Path, target_dir: Path):
    """Копіює файл у підпапку за його розширенням."""
    try:
        # Визначаємо розширення файлу, якщо немає — кладемо в "unknown"
        ext = file_path.suffix.lower()[1:] if file_path.suffix else "unknown"
        ext_dir = target_dir / ext
        ext_dir.mkdir(parents=True, exist_ok=True)

        # Копіюємо файл у потрібну папку
        shutil.copy2(file_path, ext_dir / file_path.name)
        print(f"✔ Скопійовано: {file_path} → {ext_dir}")
    except Exception as e:
        print(f"❌ Помилка копіювання {file_path}: {e}")


def collect_files(src_dir: Path):
    """Збирає список усіх файлів у папці та підпапках."""
    files = []
    for root, _, filenames in os.walk(src_dir):
        for name in filenames:
            files.append(Path(root) / name)
    return files


def sort_files_by_extension():
    """Запускає сортування файлів за розширеннями з використанням потоків."""
    print("\n=== СОРТУВАННЯ ФАЙЛІВ ===")
    src_path = input("Введіть шлях до вихідної папки: ").strip()
    target_path = input("Введіть шлях до папки для сортування (Enter = dist): ").strip() or "dist"

    src_dir = Path(src_path)
    target_dir = Path(target_path)

    if not src_dir.exists() or not src_dir.is_dir():
        print(f"❌ Помилка: папка {src_dir} не існує!")
        return

    files = collect_files(src_dir)
    print(f"🔍 Знайдено {len(files)} файлів. Починаю копіювання...\n")

    start = time.time()
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(copy_file, file, target_dir) for file in files]
        for future in as_completed(futures):
            future.result()

    print(f"\n✅ Сортування завершено за {time.time() - start:.2f} сек.")


# =====================================================================
#                ЧАСТИНА 2 — FACTORIZE (ПРОЦЕСИ)
# =====================================================================

def find_divisors(number: int):
    """Знаходить усі дільники числа."""
    return [i for i in range(1, number + 1) if number % i == 0]


def factorize_sync(*numbers):
    """Синхронна версія factorize."""
    results = []
    for number in numbers:
        results.append(find_divisors(number))
    return results


def factorize_parallel(*numbers):
    """Паралельна версія factorize з використанням процесів."""
    with Pool(cpu_count()) as pool:
        results = pool.map(find_divisors, numbers)
    return results


def run_factorize():
    """Запускає обчислення дільників із вимірюванням часу."""
    print("\n=== ОБЧИСЛЕННЯ ДІЛЬНИКІВ ===")
    nums = input("Введіть числа через пробіл: ").strip()
    numbers = tuple(map(int, nums.split()))

    # --- Синхронна версія ---
    print("\n🔹 Синхронна версія:")
    start = time.time()
    results_sync = factorize_sync(*numbers)
    sync_time = time.time() - start
    for num, divisors in zip(numbers, results_sync):
        print(f"Число {num}: {divisors}")
    print(f"⏱ Час виконання: {sync_time:.2f} сек")

    # --- Паралельна версія ---
    print("\n🔹 Паралельна версія:")
    start = time.time()
    results_parallel = factorize_parallel(*numbers)
    parallel_time = time.time() - start
    for num, divisors in zip(numbers, results_parallel):
        print(f"Число {num}: {divisors}")
    print(f"⏱ Час виконання: {parallel_time:.2f} сек")

    # --- Порівняння швидкості ---
    speedup = sync_time / parallel_time if parallel_time > 0 else 1
    print(f"\n⚡ Прискорення: у {speedup:.2f} разів швидше!")


# =====================================================================
#                МЕНЮ ПРОГРАМИ
# =====================================================================

def main_menu():
    while True:
        print("\n" + "="*50)
        print("        ДОМАШНЄ ЗАВДАННЯ №3")
        print("="*50)
        print("1 — Сортування файлів за розширеннями (потоки)")
        print("2 — Factorize (пошук дільників, процеси)")
        print("3 — Вихід")
        print("="*50)

        choice = input("Виберіть дію: ").strip()

        if choice == "1":
            sort_files_by_extension()
        elif choice == "2":
            run_factorize()
        elif choice == "3":
            print("👋 Вихід із програми.")
            break
        else:
            print("❌ Помилка: введіть число 1, 2 або 3.")


if __name__ == "__main__":
    main_menu()
