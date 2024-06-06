import difflib

from .models import Unnecessary_word_filter


def similar(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()


def clean_similar_text(caption, text, similarity_threshold=0.7):
    # Qatorlarni ajratib olib, ma'lumotlardan iborat bo'lgan qatorlarni tekshirish
    caption_lines = caption.split('\n')
    for i, line in enumerate(caption_lines):
        # O'xshashlik darajasini aniqlash
        similarity_ratio = similar(line, text)
        print("Similarity ratio:", similarity_ratio)

        # Agar o'xshashlik belgilangan cheklovni tushsa, qatorni o'chirish
        if similarity_ratio >= similarity_threshold:
            caption_lines[i] = ""

    # O'chirilgan qatorlarni to'plab qaytaramiz
    cleaned_caption = '\n'.join(caption_lines)

    return cleaned_caption.strip()


def remove_empty_lines(text):
    # Matnni qatorlarga ajratamiz
    lines = text.split("\n")

    # Bo'sh qatorlarni o'chiramiz
    non_empty_lines = [line for line in lines if line.strip()]

    # Qatorlarni qaytarib bering
    return "\n".join(non_empty_lines)


def clean_caption(caption):
    # Barcha kerakli so'zlar
    if Unnecessary_word_filter.objects.count() == 0:
        print("[INFO] No unnecessary words found in the database")
        return caption
    words = Unnecessary_word_filter.objects.values_list('word', flat=True)
    # So'zlar bilan tekshirish
    for word in words:
        caption = clean_similar_text(caption, word)

    # Tekshirilgan matnni qaytarish
    caption=remove_empty_lines(caption)
    return caption
