import random
import numpy as np
import string
from hashbase import RIPEMD320
import scipy.stats as stats
import matplotlib.pyplot as plt

base_message = "NedashkivskaArinaVitalyivna"

def HashGeneration(message):
    return RIPEMD320().generate_hash(message)

def generate_random_suffix(length=4):
    return ''.join(random.choices('0123456789', k=length))

def modify_message_randomly(message):
    message_list = list(message)
    idx = random.randint(0, len(message) - 1) 
    new_char = random.choice(string.ascii_letters + string.digits + "!@#$%^&*()-_=+[{]}|;:'\",<.>/?")
    message_list[idx] = new_char
    return ''.join(message_list)


def preimage_attack_sequential(original_message, original_hash, bits=16, detailed=False):
    target_suffix = original_hash[-bits // 4:]  
    iteration = 0

    if detailed:
        print("\nПерші 30 повідомлень та їх геші (Перша атака пошуку прообразу):")  

    while True:
        iteration += 1
        test_message = f"{original_message}{iteration}"
        test_hash = HashGeneration(test_message)
        if detailed and iteration <= 30:
            print(f"{iteration}: {test_message} -> {test_hash}")
        if test_hash[-bits // 4:] == target_suffix:
            if detailed:
                return iteration, test_message, test_hash, target_suffix
            else:
                return iteration


def preimage_attack_random_modifications(original_message, original_hash, bits=16, detailed=False):
    target_suffix = original_hash[-bits // 4:] 
    iteration = 0
    current_message = original_message

    if detailed:
        print("\nПерші 30 повідомлень та їх геші (Друга атака пошуку прообразу):")  

    while True:
        iteration += 1
        current_message = modify_message_randomly(current_message)
        test_hash = HashGeneration(current_message)
        if detailed and iteration <= 30:
            print(f"{iteration}: {current_message} -> {test_hash}")
        if test_hash[-bits // 4:] == target_suffix:
            if detailed:
                return iteration, current_message, test_hash, target_suffix
            else:
                return iteration

def birthday_attack_sequential(original_message, bits=32, detailed=False):
    iteration = 0
    hash_map = {} 
    target_suffix_length = bits // 4  

    if detailed:
        print("\nПерші 30 повідомлень та їх геші (Перша атака 'днiв народжень'):")

    while True:
        iteration += 1
        test_message = f"{original_message}{iteration}"
        test_hash = HashGeneration(test_message)
        suffix = test_hash[-target_suffix_length:]  
        if detailed and iteration <= 30:
            print(f"{iteration}: {test_message} -> {test_hash}")
        if suffix in hash_map:
            previous_message = hash_map[suffix]
            if detailed:
                return iteration, test_message, test_hash, previous_message, suffix
            else:
                return iteration

        hash_map[suffix] = test_message


def birthday_attack_random_modifications(original_message, bits=32, detailed=False):
    iteration = 0
    hash_map = {} 
    target_suffix_length = bits // 4  

    if detailed:
        print("\nПерші 30 повідомлень та їх геші (Друга атака 'днiв народжень'):")

    while True:
        iteration += 1
        modified_message = modify_message_randomly(original_message)
        test_hash = HashGeneration(modified_message)
        suffix = test_hash[-target_suffix_length:]
        if detailed and iteration <= 30:
            print(f"{iteration}: {modified_message} -> {test_hash}")
        if suffix in hash_map and hash_map[suffix] != modified_message:
            previous_message = hash_map[suffix]
            collision_message1 = modified_message
            collision_message2 = previous_message
            if detailed:
                return iteration, collision_message1, collision_message2, test_hash, suffix
            else:
                return iteration

        hash_map[suffix] = modified_message
        original_message = modified_message



print("\n==== Результати Перша атака пошуку прообразу: ===")
random_suffix_1 = generate_random_suffix()
message_1 = f"{base_message}{random_suffix_1}"
original_hash_1 = HashGeneration(message_1)
print(f"Сформоване повідомлення для Перша атака пошуку прообразу: {message_1}")
print(f"Зафіксоване геш-значення для Перша атака пошуку прообразу: {original_hash_1}")
iterations1, found_message1, found_hash1, target_suffix1 = preimage_attack_sequential(message_1, original_hash_1, detailed=True)
print("\nРезультати Перша атака пошуку прообразу:")
print(f"Кількість ітерацій: {iterations1}")
print(f"Шуканий суфікс: {target_suffix1}")
print(f"Знайдене повідомлення: {found_message1}")
print(f"Геш знайденого повідомлення: {found_hash1}")


print("\n=== Результати Друга атака пошуку прообразу: ===")
random_suffix_2 = generate_random_suffix()
message_2 = f"{base_message}{random_suffix_2}"
original_hash_2 = HashGeneration(message_2)
print(f"Сформоване повідомлення для Друга атака пошуку прообразу: {message_2}")
print(f"Зафіксоване геш-значення для Друга атака пошуку прообразу: {original_hash_2}")
iterations2, found_message2, found_hash2, target_suffix2 = preimage_attack_random_modifications(message_2, original_hash_2, detailed=True)
print("\nРезультати Друга атака пошуку прообразу:")
print(f"Кількість ітерацій: {iterations2}")
print(f"Шуканий суфікс: {target_suffix2}")
print(f"Знайдене повідомлення: {found_message2}")
print(f"Геш знайденого повідомлення: {found_hash2}")


print("\n=== Результати Перша атака 'днiв народжень': ===")
random_suffix_3 = generate_random_suffix()
message_3 = f"{base_message}{random_suffix_3}"
original_hash_3 = HashGeneration(message_3)
print(f"Сформоване повідомлення для Перша атака 'днiв народжень': {message_3}")
print(f"Зафіксоване геш-значення для Перша атака 'днiв народжень': {original_hash_3}")
iterations3, collision_message1, collision_hash1, collision_message2, collision_suffix = birthday_attack_sequential(message_3, detailed=True)
print("\nРезультати Перша атака 'днiв народжень':")
print(f"Кількість ітерацій: {iterations3}")
print(f"Шуканий суфікс: {collision_suffix}")
print(f"Перше повідомлення: {collision_message1}")
print(f"Друге повідомлення: {collision_message2}")
print(f"Геш першого повідомлення: {collision_hash1}")
print(f"Геш другого повідомлення: {HashGeneration(collision_message2)}")


print("\n=== Результати Друга атака 'днiв народжень': ===")
random_suffix_4 = generate_random_suffix()
message_4 = f"{base_message}{random_suffix_4}"
original_hash_4 = HashGeneration(message_4)
print(f"Сформоване повідомлення для Друга атака 'днiв народжень': {message_4}")
print(f"Зафіксоване геш-значення для Друга атака 'днiв народжень': {original_hash_4}")
iterations4, collision_message1, collision_message2, collision_hash, collision_suffix = birthday_attack_random_modifications(message_4, detailed=True)
print("\nРезультати Друга атака 'днiв народжень':")
print(f"Кількість ітерацій: {iterations4}")
print(f"Шуканий суфікс: {collision_suffix}")
print(f"Перше повідомлення: {collision_message1}")
print(f"Друге повідомлення: {collision_message2}")
print(f"Геш першого повідомлення: {collision_hash}")
print(f"Геш другого повідомлення: {HashGeneration(collision_message2)}")







# def calculate_statistics(iterations_list):
#     mean = np.mean(iterations_list)
#     variance = np.var(iterations_list)
#     std_dev = np.std(iterations_list)
#     confidence_interval = stats.t.interval(0.95, len(iterations_list)-1, loc=mean, scale=std_dev/np.sqrt(len(iterations_list)))
    
#     return mean, variance, confidence_interval

# iterations_1 = []
# iterations_2 = []
# iterations_3 = []
# iterations_4 = []

# print("\n=== 100 запусків ===")
# for run in range(1, 101):
#     random_suffix_1 = generate_random_suffix()
#     message_1 = f"{base_message}{random_suffix_1}"
#     original_hash_1 = HashGeneration(message_1)
#     iterations1 = preimage_attack_sequential(message_1, original_hash_1)
    
#     random_suffix_2 = generate_random_suffix()
#     message_2 = f"{base_message}{random_suffix_2}"
#     original_hash_2 = HashGeneration(message_2)
#     iterations2 = preimage_attack_random_modifications(message_2, original_hash_2)

#     random_suffix_3 = generate_random_suffix()
#     message_3 = f"{base_message}{random_suffix_3}"
#     original_hash_3 = HashGeneration(message_3)
#     iterations3 = birthday_attack_sequential(message_3)

#     random_suffix_4 = generate_random_suffix()
#     message_4 = f"{base_message}{random_suffix_4}"
#     original_hash_4 = HashGeneration(message_4)
#     iterations4 = birthday_attack_random_modifications(message_4)

#     iterations_1.append(iterations1)
#     iterations_2.append(iterations2)
#     iterations_3.append(iterations3)
#     iterations_4.append(iterations4)


#     print(f"Запуск {run}, Кількість ітерацій (Перша атака пошуку прообразу) - {iterations1}")
#     print(f"Запуск {run}, Кількість ітерацій (Друга атака пошуку прообразу) - {iterations2}")
#     print(f"Запуск {run}, Кількість ітерацій (Перша атака 'днiв народжень') - {iterations3}")
#     print(f"Запуск {run}, Кількість ітерацій (Друга атака 'днiв народжень') - {iterations4}")

# mean_1, var_1, conf_interval_1 = calculate_statistics(iterations_1)
# mean_2, var_2, conf_interval_2 = calculate_statistics(iterations_2)
# mean_3, var_3, conf_interval_3 = calculate_statistics(iterations_3)
# mean_4, var_4, conf_interval_4 = calculate_statistics(iterations_4)

# print("\n=== Статистика для кожної атаки ===")
# print(f"Перша атака пошуку прообразу - Середнє значення: {mean_1}, Дисперсія: {var_1}, Довірчий інтервал: {conf_interval_1}")
# print(f"Друга атака пошуку прообразу - Середнє значення: {mean_2}, Дисперсія: {var_2}, Довірчий інтервал: {conf_interval_2}")
# print(f"Перша атака 'днiв народжень'- Середнє значення: {mean_3}, Дисперсія: {var_3}, Довірчий інтервал: {conf_interval_3}")
# print(f"Друга атака 'днiв народжень' - Середнє значення: {mean_4}, Дисперсія: {var_4}, Довірчий інтервал: {conf_interval_4}")


# def plot_histogram(iterations, title):
#     plt.figure(figsize=(10, 6))
#     plt.hist(iterations, bins=20, edgecolor='red', alpha=0.7)
#     plt.title(f"Гістограма для {title}")
#     plt.xlabel('Кількість ітерацій')
#     plt.ylabel('Частота')
#     plt.grid(True)
#     plt.show()

# plot_histogram(iterations_1, 'Атака 1')
# plot_histogram(iterations_2, 'Атака 2')
# plot_histogram(iterations_3, 'Атака 3')
# plot_histogram(iterations_4, 'Атака 4')