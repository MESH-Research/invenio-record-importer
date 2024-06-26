"""A dictionary of month names in various languages and their corresponding two-digit month numbers.

Covers the following languages: English, French, Spanish, Portuguese, Hebrew, Arabic, Russian, Mandarin Chinese, Japanese, German, Bengali, Urdu, Telugu, Indonesian, Turkish, Hindi, Marathi, Tamil, Dutch, Italian, Polish, Swedish, Danish, Irish, Javanese, Korean, Gujarati, Ukranian.

FIXME: Cover more languages.
"""

monthwords = {
    "january": "01",
    "february": "02",
    "march": "03",
    "april": "04",
    "may": "05",
    "june": "06",
    "july": "07",
    "august": "08",
    "september": "09",
    "october": "10",
    "november": "11",
    "december": "12",
    "janvier": "01",
    "enero": "01",
    "janeiro": "01",
    "ינואר": "01",
    "يناير": "01",
    "январь": "01",
    "一月": "01",
    "Januar": "01",
    "février": "02",
    "febrero": "02",
    "fevereiro": "02",
    "פברואר": "02",
    "فبراير": "02",
    "февраль": "02",
    "二月": "02",
    "Februar": "02",
    "mars": "03",
    "marzo": "03",
    "março": "03",
    "מרץ": "03",
    "مارس": "03",
    "март": "03",
    "三月": "03",
    "März": "03",
    "avril": "04",
    "abril": "04",
    "abril": "04",
    "אפריל": "04",
    "أبريل": "04",
    "апрель": "04",
    "四月": "04",
    "April": "04",
    "mai": "05",
    "mayo": "05",
    "maio": "05",
    "מאי": "05",
    "مايو": "05",
    "май": "05",
    "五月": "05",
    "Mai": "05",
    "juin": "06",
    "junio": "06",
    "junho": "06",
    "יוני": "06",
    "يونيو": "06",
    "июнь": "06",
    "六月": "06",
    "Juni": "06",
    "juillet": "07",
    "julio": "07",
    "julho": "07",
    "יולי": "07",
    "يوليو": "07",
    "июль": "07",
    "七月": "07",
    "Juli": "07",
    "août": "08",
    "agosto": "08",
    "agosto": "08",
    "אוגוסט": "08",
    "أغسطس": "08",
    "август": "08",
    "八月": "08",
    "August": "08",
    "septembre": "09",
    "septiembre": "09",
    "setembro": "09",
    "ספטמבר": "09",
    "سبتمبر": "09",
    "сентябрь": "09",
    "九月": "09",
    "September": "09",
    "octobre": "10",
    "octubre": "10",
    "outubro": "10",
    "אוקטובר": "10",
    "أكتوبر": "10",
    "октябрь": "10",
    "十月": "10",
    "Oktober": "10",
    "novembre": "11",
    "noviembre": "11",
    "novembro": "11",
    "נובמבר": "11",
    "نوفمبر": "11",
    "ноябрь": "11",
    "十一月": "11",
    "November": "11",
    "décembre": "12",
    "diciembre": "12",
    "dezembro": "12",
    "דצמבר": "12",
    "ديسمبر": "12",
    "декабрь": "12",
    "十二月": "12",
    "Dezember": "12",
    "জানুয়ারী": "01",
    "جنوری": "01",
    "一月": "01",
    "జనవరి": "01",
    "Januari": "01",
    "Ocak": "01",
    "जनवरी": "01",
    "जानेवारी": "01",
    "ஜனவரி": "01",
    "ফেব্রুয়ারী": "02",
    "فروری": "02",
    "二月": "02",
    "ఫిబ్రవరి": "02",
    "Februari": "02",
    "Şubat": "02",
    "फ़रवरी": "02",
    "फेब्रुवारी": "02",
    "பிப்ரவரி": "02",
    "মার্চ": "03",
    "مارچ": "03",
    "三月": "03",
    "మార్చి": "03",
    "Maret": "03",
    "Mart": "03",
    "मार्च": "03",
    "मार्च": "03",
    "மார்ச்": "03",
    "এপ্রিল": "04",
    "اپریل": "04",
    "四月": "04",
    "ఏప్రిల్": "04",
    "April": "04",
    "Nisan": "04",
    "अप्रैल": "04",
    "एप्रिल": "04",
    "ஏப்ரல்": "04",
    "মে": "05",
    "مئی": "05",
    "五月": "05",
    "మే": "05",
    "Mei": "05",
    "Mayıs": "05",
    "मई": "05",
    "मे": "05",
    "மே": "05",
    "জুন": "06",
    "جون": "06",
    "六月": "06",
    "జూన్": "06",
    "Juni": "06",
    "Haziran": "06",
    "जून": "06",
    "जून": "06",
    "ஜூன்": "06",
    "জুলাই": "07",
    "جولائی": "07",
    "七月": "07",
    "జూలై": "07",
    "Juli": "07",
    "Temmuz": "07",
    "जुलाई": "07",
    "जुलै": "07",
    "ஜூலை": "07",
    "আগস্ট": "08",
    "اگست": "08",
    "八月": "08",
    "ఆగష్టు": "08",
    "Agustus": "08",
    "Ağustos": "08",
    "अगस्त": "08",
    "ऑगस्ट": "08",
    "ஆகஸ்ட்": "08",
    "সেপ্টেম্বর": "09",
    "ستمبر": "09",
    "九月": "09",
    "సెప్టెంబర్": "09",
    "September": "09",
    "Eylül": "09",
    "सितंबर": "09",
    "सप्टेंबर": "09",
    "செப்டம்பர்": "09",
    "অক্টোবর": "10",
    "اکتوبر": "10",
    "十月": "10",
    "అక్టోబర్": "10",
    "Oktober": "10",
    "Ekim": "10",
    "अक्टूबर": "10",
    "ऑक्टोबर": "10",
    "அக்டோபர்": "10",
    "নভেম্বর": "11",
    "نومبر": "11",
    "十一月": "11",
    "నవంబర్": "11",
    "November": "11",
    "Kasım": "11",
    "नवंबर": "11",
    "नोव्हेंबर": "11",
    "நவம்பர்": "11",
    "ডিসেম্বর": "12",
    "دسمبر": "12",
    "十二月": "12",
    "డిసెంబర్": "12",
    "Desember": "12",
    "Aralık": "12",
    "दिसंबर": "12",
    "डिसेंबर": "12",
    "டிசம்பர்": "12",
    "januari": "01",
    "gennaio": "01",
    "styczeń": "01",
    "januari": "01",
    "januar": "01",
    "Eanáir": "01",
    "Januari": "01",
    "1월": "01",
    "જાન્યુઆરી": "01",
    "січень": "01",
    "februari": "02",
    "febbraio": "02",
    "luty": "02",
    "februari": "02",
    "februar": "02",
    "Feabhra": "02",
    "Februari": "02",
    "2월": "02",
    "ફેબ્રુઆરી": "02",
    "лютий": "02",
    "maart": "03",
    "marzo": "03",
    "marzec": "03",
    "mars": "03",
    "marts": "03",
    "Márta": "03",
    "Maret": "03",
    "3월": "03",
    "માર્ચ": "03",
    "березень": "03",
    "april": "04",
    "aprile": "04",
    "kwiecień": "04",
    "april": "04",
    "april": "04",
    "Aibreán": "04",
    "April": "04",
    "4월": "04",
    "એપ્રિલ": "04",
    "квітень": "04",
    "mei": "05",
    "maggio": "05",
    "maj": "05",
    "maj": "05",
    "maj": "05",
    "Bealtaine": "05",
    "Mei": "05",
    "5월": "05",
    "મે": "05",
    "травень": "05",
    "juni": "06",
    "giugno": "06",
    "czerwiec": "06",
    "juni": "06",
    "juni": "06",
    "Meitheamh": "06",
    "Juni": "06",
    "6월": "06",
    "જૂન": "06",
    "червень": "06",
    "juli": "07",
    "luglio": "07",
    "lipiec": "07",
    "juli": "07",
    "juli": "07",
    "Iúil": "07",
    "Juli": "07",
    "7월": "07",
    "જુલાઈ": "07",
    "липень": "07",
    "augustus": "08",
    "agosto": "08",
    "sierpień": "08",
    "augusti": "08",
    "august": "08",
    "Lúnasa": "08",
    "Agustus": "08",
    "8월": "08",
    "ઓગસ્ટ": "08",
    "серпень": "08",
    "september": "09",
    "settembre": "09",
    "wrzesień": "09",
    "september": "09",
    "september": "09",
    "Meán Fómhair": "09",
    "September": "09",
    "9월": "09",
    "સપ્ટેમ્બર": "09",
    "вересень": "09",
    "oktober": "10",
    "ottobre": "10",
    "październik": "10",
    "oktober": "10",
    "oktober": "10",
    "Deireadh Fómhair": "10",
    "Oktober": "10",
    "10월": "10",
    "ઓક્ટોબર": "10",
    "жовтень": "10",
    "november": "11",
    "novembre": "11",
    "listopad": "11",
    "november": "11",
    "november": "11",
    "Samhain": "11",
    "November": "11",
    "11월": "11",
    "નવેમ્બર": "11",
    "листопад": "11",
    "december": "12",
    "dicembre": "12",
    "grudzień": "12",
    "december": "12",
    "december": "12",
    "Nollaig": "12",
    "Desember": "12",
    "12월": "12",
    "ડિસેમ્બર": "12",
    "грудень": "12",
}
