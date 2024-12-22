import random
from hashbase import RIPEMD320
from concurrent.futures import ThreadPoolExecutor

N = 10000
n = 16

def generate_random(bit_length):
    return random.randbytes(bit_length // 8)

def get_hash(message):
    if isinstance(message, int):
        message = hex(message)[2:]  
    if isinstance(message, bytes):
        message_str = message.hex()
    else:
        message_str = message

    hash_value = RIPEMD320().generate_hash(message_str)
    return bytes.fromhex(hash_value)

def redundancy_function(x, r):
    return (r + x)


def generate_table(K, L, r =None):
    if r is None:
        r = generate_random(128 - n)
    X = {}

    for i in range(K):
        x_i0 = generate_random(n)
        x_ij = x_i0
        for j in range(L):
            x_ij = get_hash(redundancy_function(x_ij, r))[-(n // 8):]
        X[x_ij] = x_i0

    sorted_X = dict(sorted(X.items()))
    return sorted_X, r


def find_preimage(L, table, hash_value):
    y = hash_value[-(n // 8):]
    X = table[0]
    r = table[1]

    for j in range(L):
        if y in X:
            x = X[y]
            for m in range(L - j - 1):
                x = get_hash(redundancy_function(x, r))[-(n // 8):]
            return redundancy_function(x, r)
        y = get_hash(redundancy_function(y, r))[-(n // 8):]
    return 0



#          АТАКА 1

K = [2**10, 2**12, 2**14]  
L = [2**5, 2**6, 2**7]  

def attack1_N():
    result = {
        'keys': [],
        'successes': [],
        'fails': [],
    }
    
    for k in K:
        for l in L:
            table = generate_table(k, l)
            success = 0
            fail = 0
            first_success = False 
            
            for attempt in range(N):
                vector = generate_random(256)
                hash_result = get_hash(vector)
                preimage = find_preimage(l, table, hash_result)

                if preimage:
                    preimage_hash = get_hash(preimage)

                    if preimage_hash[-(n // 8):] == hash_result[-(n // 8):]:
                        success += 1
                        if not first_success:
                            print(f"Перший успіх на спробі {attempt + 1}:")
                            print(f"Випадковий вектор: {vector.hex()}")
                            print(f"Хеш вектора: {hash_result.hex()}")
                            print(f"Прообраз: {preimage.hex()}")
                            print(f"Хеш прообразу: {preimage_hash.hex()}")
                            first_success = True 
                    else:
                        fail += 1
                else:
                    fail += 1

            result['keys'].append((k, l))
            result['successes'].append(success)
            result['fails'].append(fail)

            print(f"K: {k}, L: {l}:") 
            print(f"Успіх: {success}, Невдача: {fail}")
            print(f"_______________________________________________________________________________________")

    return result
attack1_N()



#           АТАКА 2 (краще не запускати)


# def super_generate_tables(K, L, r=None):
#     tables = []
#     with ThreadPoolExecutor() as executor:
#         futures = [executor.submit(generate_table, K, L, r) for _ in range(K)]  
#         for future in futures:
#             table, r_used = future.result()
#             tables.append((table, r_used))
#     return tables

# def super_find_preimages(L, tables, hash_value):
#     results = []
#     with ThreadPoolExecutor() as executor:
#         futures = [executor.submit(find_preimage, L, tables[i], hash_value) for i in range(len(tables))]
#         for future in futures:
#             results.append(future.result())
#     return results


# K_values = [2**5, 2**6, 2**7]
# L_values = [2**4, 2**5, 2**6]

# def attack_2_N():
#     result = {
#         'keys': [],
#         'successes': [],
#         'fails': [],
#         'tables_generated': [],
#         'redundancy_functions': [],
#     }

#     for k in K_values:
#         for l in L_values:
#             tables = super_generate_tables(k, l)  
#             # tables_generated = len(tables)  
#             # result['tables_generated'].append(tables_generated)
#             success = 0
#             fail = 0

#             # redundancy_functions = [r for _, r in tables]
#             # result['redundancy_functions'].append(redundancy_functions)

#             for _ in range(N):  
#                 vector = generate_random(256)
#                 hash_result = get_hash(vector)
#                 preimages = super_find_preimages(l, tables, hash_result) 
                
#                 if preimages:
#                     found_valid_preimage = False
#                     for preimage in preimages:
#                         preimage_hash = get_hash(preimage)
#                         if preimage_hash[-(n // 8):] == hash_result[-(n // 8):]:
#                             success += 1
#                             found_valid_preimage = True
#                             break
#                     if not found_valid_preimage:
#                         fail += 1  
#                 else:
#                     fail += 1  

#             result['keys'].append((k, l))
#             result['successes'].append(success)
#             result['fails'].append(fail)

#             print(f"K: {k}, L: {l}:") 
#             print(f"Успіх: {success}, Невдача: {fail}")
#             # print(f"Кількість згенерованих таблиць: {tables_generated}")
#             # print(f"Функції надлишковості: {redundancy_functions}")  
#             print(f"_______________________________________________________________________________________")

#     return result

# attack_2_N()
