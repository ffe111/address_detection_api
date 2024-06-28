from thaiAddressTag.hashmaps import hashmap
from thaiAddressTag.addresses import address_list
from thaiAddressTag.utils import *

from pythainlp.util import dict_trie
from pythainlp.corpus.common import thai_words
from pythainlp import Tokenizer
from pythainlp.spell import NorvigSpellChecker

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)


def find_address_match(address_list, text_list):
    """
      find address match
      update
       - แก้อำเภอเมือง
       - ตรวจสอบหาจังหวัดน่านได้

    """
    best_match = {
        'province': None,
        'amphoe': None,
        'district': None,
        'zipcode': None
    }

    possible_provinces = []

    # Check province and insert to list
    for text in text_list:
        if text in address_list:
            possible_provinces.append(text)

    # Check and correct for 'เมือง'
    for province in possible_provinces:
        for i, text in enumerate(text_list):
            if text == 'เมือง' and province != 'ศรีสะเกษ':
                text_list[i] = 'เมือง' + province
                break

    # Initialize potential matches
    district_matches = []
    amphoe_matches = []
    zipcode_matches = []

    # Collect all matches first
    for province in possible_provinces:
        for text in text_list:
            for amphoe in address_list[province]:
                for subdistrict, postcode in address_list[province][amphoe]:
                    if text == subdistrict:
                        district_matches.append(
                            (province, amphoe, subdistrict))
                    if text == postcode:
                        zipcode_matches.append((province, amphoe, postcode))
                if text == amphoe:
                    amphoe_matches.append((province, amphoe))

    # Determine best matches based on collected data
    # Prioritize the full match with district and zipcode
    for province, amphoe, subdistrict in district_matches:
        for p, a, z in zipcode_matches:
            if province == p and amphoe == a:
                best_match['province'] = province
                best_match['amphoe'] = amphoe
                best_match['district'] = subdistrict
                best_match['zipcode'] = z
                return best_match

    # If full match not found, prioritize district and amphoe
    for province, amphoe, subdistrict in district_matches:
        best_match['province'] = province
        best_match['amphoe'] = amphoe
        best_match['district'] = subdistrict
        break  # Take the first match

    # If no district match, prioritize amphoe and zipcode
    for province, amphoe in amphoe_matches:
        for p, a, z in zipcode_matches:
            if province == p and amphoe == a:
                best_match['province'] = province
                best_match['amphoe'] = amphoe
                best_match['zipcode'] = z
                return best_match

    # If no full match, take first amphoe match
    for province, amphoe in amphoe_matches:
        if not best_match['amphoe']:
            best_match['province'] = province
            best_match['amphoe'] = amphoe
            break  # Take the first match

    # If no amphoe match, take first zipcode match
    for province, amphoe, postcode in zipcode_matches:
        if not best_match['zipcode']:
            best_match['province'] = province
            best_match['amphoe'] = amphoe
            best_match['zipcode'] = postcode
            break  # Take the first match

    return best_match


def initial_nlp_tools(hashmap):
    """
    create pythainlp tools
    word tokenize and spellchecker
    """
    # custom_word_lists = set(thai_words())
    # custom_word_lists.update(list(hashmap.keys()))

    custom_word_lists = set(list(hashmap.keys()))
    addtexts = ["หมู่", "ม.", "ถนน", "ซอย", "ซ.",
                "ตำบล", "ต.", "อำเภอ", "อ.", "จ.", "จังหวัด"]
    custom_word_lists.update(addtexts)
    # BoW for word tokenize
    trie = dict_trie(dict_source=custom_word_lists)
    # Create Tokenizer
    custom_tokenize = Tokenizer(
        custom_dict=trie, join_broken_num=False, keep_whitespace=False, engine='newmm')

    custom_checker_list = set(list(hashmap.keys()))
    addtexts = ["หมู่", "ม.", "ถนน", "ซอย", "ซ.",
                "ตำบล", "ต.", "อำเภอ", "อ.", "จ.", "จังหวัด"]
    custom_checker_list.update(addtexts)
    # BoW for word spellchecker
    ctrie = dict_trie(dict_source=custom_checker_list)
    # Create SpellChecker
    checker = NorvigSpellChecker(
        custom_dict=ctrie, min_freq=1, min_len=5, max_len=30)
    return custom_tokenize, checker


def extract_address(text, custom_tokenize, checker, address_list=address_list):
    """
    extract address
    update
     - แก้คำผิด จะไม่แก้พวกชื่อจังหวัด เนื่องจาก เคสชื่อจังหวัดน่าน ผิด
    """
    # result format
    matching_result = {
        'province': None,
        'amphoe': None,
        'district': None,
        'zipcode': None,
        'name': None,
        'phone': None
    }

    # text process
    text = text.replace("นาย ", "นาย")
    text = text.replace("นางสาว ", "นางสาว")
    text = text.replace("นาง ", "นาง")
    text = text.replace("คุณ ", "คุณ")

    text = preprocess(text)
    text = clean_location_text(text)
    # extract and update matching {name, phone} data
    text, name = extract_name(text)
    text, phone = extract_phone(text)
    if name != None:
        matching_result['name'] = name
    if phone != None:
        matching_result['phone'] = phone

    # tokenize text
    # tokenize_texts = custom_tokenize.word_tokenize(text)
    # spell checker
    # word_lists = [checker.correct(token) for token in tokenize_texts
    #               if token not in ["หมู่", "ม.", "ถนน", "ซอย", "ซ.", "ตำบล", "ต.", "อำเภอ", "อ.", "จ.", "จังหวัด"]
    #               and token not in address_list.keys()]
    # tokenize text
    tokenize_texts = custom_tokenize.word_tokenize(text)
    # spell checker
    word_lists = [checker.correct(token) if token not in ["หมู่", "ม.", "ถนน", "ซอย", "ซ.", "ตำบล", "ต.", "อำเภอ", "อ.", "จ.", "จังหวัด"]
                  and token not in address_list.keys() else token for token in tokenize_texts]
    # print(word_lists)
    result = find_address_match(address_list, word_lists)
    # print(result)
    # update data
    matching_result.update(result)

    return matching_result
