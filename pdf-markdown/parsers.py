import re
from urllib.parse import urlparse

from core import MDTable

empty_space_replace_regex = re.compile(r"[\n\r\t]+")

def phone_or_str(x):
    if x == "None" or x is None or x == "" or x == "-":
        return "-"
    
    if "-" in x:
        return x

    return f"[{x}](tel:{x.replace(' ', '')})"

def link_or_str(x, label):
    p = urlparse(x)

    if "Ücretsiz Ekmek" in x:
        print("\n\nDEBUG: ", x, p, "\n")

    if p.scheme == "" or p.netloc == "":
        return x
    
    return f"[{label}]({x})"

def str_or_list(x):
    if isinstance(x, list):
        return ", ".join(x)
    else:
        return str(x).strip()

def process_rows(r):
    rr =  list(map(str.strip, map(str, r.values())))

    rows = []

    for i in range(len(rr)):
        if rr[i] == "None" or rr[i] is None:
            rows.append("-")
        else:
            #rows.append(rr[i].replace("\n", " - "))
            rows.append(empty_space_replace_regex.sub(" - ", rr[i]))
    
    return rows

def process_rows_list(r):
    rr = list(map(str_or_list, r.values()))

    rows = []

    for i in range(len(rr)):
        if rr[i] == "None" or rr[i] is None:
            rows.append("-")
        else:
            # rows.append(rr[i].replace("\n", " - "))
            rows.append(empty_space_replace_regex.sub(" - ", rr[i]))

    return rows

def parse_city_accom(data):
    rows = []

    for r in data["items"]:
        rr = process_rows(r)

        if rr[2] != "-":
            rr[2] = "Doğrulanmış" if rr[2] == "True" else "Doğrulanmamış"
        
        if rr[3] != "-":
            rr[3] = link_or_str(rr[3], "Kaynak")
        
        if rr[4] != "-":
            rr[4] = link_or_str(rr[4], "Google Maps")

        rows.append(rr)

    return MDTable(["Şehir", "Yer", "Doğrulanma Durumu", "Kaynak", "Adres", "Doğrulanma Tarihi"], rows)

def parse_gathering(data):
    rows = []

    for r in data["items"]:
        rr = process_rows(r)

        if rr[1] != "-":
            rr[1] = link_or_str(rr[1], "Google Maps")

        if rr[2] != "-":
            rr[2] = link_or_str(rr[2], "Kaynak")

        rows.append(rr)

    return MDTable(["Yer", "Harita", "Kaynak"], rows)

def parse_food(data):
    rows = []

    for r in data["items"]:
        rr = process_rows(r)

        if rr[1] != "-":
            rr[1] = link_or_str(rr[1], "Google Maps")
        
        if rr[2] != "-":
            rr[2] = link_or_str(rr[2], "Kaynak")

        rr[3] = phone_or_str(rr[3])

        rows.append(rr)

    return MDTable(["Yer", "Adres", "Kaynak", "Telefon", "Güncelleme Tarihi", "Güncelleme Saati"], rows)

def parse_pharmacy(data):
    rows = []

    for r in data["items"]:
        rr = process_rows(r)

        if rr[3] != "-":
            rr[3] = link_or_str(rr[3], "Google Maps")

        rows.append(rr)

    return MDTable(["İl", "İlçe", "Adres", "Harita"], rows)

def parse_phones(data):
    rows = []

    for r in data["phones"]:
        rr = process_rows(r)

        rr[1] = phone_or_str(rr[1])

        rows.append(rr)

    return MDTable(["İsim", "Numara"], rows)

def parse_links(data):
    rows = []

    for r in data["usefulLinks"]:
        rr = process_rows(r)

        # Extract the domain from the URL at rr[1]:
        domain = urlparse(rr[1]).netloc
        rr[1] = link_or_str(rr[1], domain)

        rows.append(rr)

    return MDTable(["İsim", "URL"], rows)

def parse_vets(data):
    rows = []

    for r in data["vets"]:
        rr = process_rows(r)

        rr[1] = phone_or_str(rr[1])
        rr[3] = link_or_str(rr[3], "Google Maps")

        rows.append(rr)

    return MDTable(["Veteriner", "Telefon", "Adres", "Harita"], rows)

def parse_help_item_list(data):
    rows = []

    for r in data["items"]:
        rr = process_rows(r)

        rr[2] = link_or_str(rr[2], "Kaynak/Harita")
        rr[3] = phone_or_str(rr[3])

        rows.append(rr)

    return MDTable(["İl", "Lokasyon", "Link", "Telefon", "Notlar"], rows)

def parse_stemcell(data):
    rows = []

    for r in data["items"]:
        rr = process_rows(r)

        rr[2] = link_or_str(rr[2], "Harita")
        rr[3] = phone_or_str(rr[3])

        rows.append(rr)

    return MDTable(["Bölge", "İl", "Adres/Harita", "Telefon"], rows)

def parse_beneficial_articles(data):
    rows = []

    for r in data["articles"]:
        rr = process_rows(r)

        domain = urlparse(rr[2]).netloc
        rr[2] = link_or_str(rr[2], domain)

        rows.append(rr)

    return MDTable(["Başlık", "Yazar", "Link", "Konu"], rows)

def parse_evacuation_points(data):
    rows = []

    for r in data["items"]:
        rr = process_rows_list(r)

        if rr[3] != "-":
            rr[3] = link_or_str(rr[3], "Google Maps")

        rows.append(rr)

    return MDTable(["İl", "İlçe", "Yer", "Harita", "Adres", "İletişim", "Kaynak"], rows)

data_type_parsers = {
    "city-accommodation": parse_city_accom,
    "new-gathering-list": parse_gathering,
    "food-items": parse_food,
    "container-pharmacy": parse_pharmacy,
    "phone-number-list": parse_phones,
    "useful-links": parse_links,
    "data-vet": parse_vets,
    "help-item-list": parse_help_item_list,
    # "blood-donationlist": lambda _: 
    "stem-cell-donation": parse_stemcell,
    "beneficial-articles": parse_beneficial_articles,
    "evacuation-points": parse_evacuation_points,
}

