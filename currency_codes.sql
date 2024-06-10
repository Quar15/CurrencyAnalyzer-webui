UPDATE currency
SET image_path = CASE code
    WHEN 'XOF' THEN 'img/flags/748001_faso_burkina_flag.png'
    WHEN 'AUD' THEN 'img/flags/748002_flag_australia.png'
    WHEN 'SLL' THEN 'img/flags/748003_flag_leone_sierra.png'
    WHEN 'CVE' THEN 'img/flags/748004_cape_verde_flag.png'
    WHEN 'EUR' THEN 'img/flags/748065_european_union_flag.png'
    WHEN 'CNY' THEN 'img/flags/748006_flag_china.png'
    WHEN 'KRW' THEN 'img/flags/748007_flag_korea_south.png'
    WHEN 'DKK' THEN 'img/flags/748008_denmark_flag.png'
    WHEN 'HRK' THEN 'img/flags/748009_flag_croatia.png'
    WHEN 'SAR' THEN 'img/flags/748010_flag_saudi_arabia.png'
    WHEN 'EGP' THEN 'img/flags/748011_flag_egypt.png'
    WHEN 'ALL' THEN 'img/flags/748013_albania_flag.png'
    WHEN 'ARS' THEN 'img/flags/748014_flag_argentina.png'
    WHEN 'CZK' THEN 'img/flags/748015_republic_czech_flag.png'
    WHEN 'CAD' THEN 'img/flags/748016_flag_canada.png'
    WHEN 'USD' THEN 'img/flags/748050_flag_usa.png'
    WHEN 'BHD' THEN 'img/flags/748019_flag_bahrain.png'
    WHEN 'CDF' THEN 'img/flags/748020_congo_flag.png'
    WHEN 'BTN' THEN 'img/flags/748021_flag_bhutan.png'
    WHEN 'BND' THEN 'img/flags/748022_brunei_flag.png'
    WHEN 'GBP' THEN 'img/flags/748024_united_kingdom_flag.png'
    WHEN 'TTD' THEN 'img/flags/748025_trinidad_tobago_flag_and.png'
    WHEN 'XOF' THEN 'img/flags/748027_bissau_flag_guinea.png'
    WHEN 'KHR' THEN 'img/flags/748028_flag_cambodia.png'
    WHEN 'KPW' THEN 'img/flags/748030_flag_north_korea.png'
    WHEN 'CUP' THEN 'img/flags/748032_flag_cuba.png'
    WHEN 'BBD' THEN 'img/flags/748035_flag_barbados.png'
    WHEN 'AWG' THEN 'img/flags/748036_aruba_flag.png'
    WHEN 'AED' THEN 'img/flags/748037_emirates_arab_united_flag.png'
    WHEN 'BGN' THEN 'img/flags/748038_bulgaria_flag.png'
    WHEN 'ISK' THEN 'img/flags/748040_flag_iceland.png'
    WHEN 'AMD' THEN 'img/flags/748041_flag_armenia.png'
    WHEN 'DZD' THEN 'img/flags/748042_algeria_flag.png'
    WHEN 'BZD' THEN 'img/flags/748043_belize_flag.png'
    WHEN 'RUB' THEN 'img/flags/748044_flag_russia.png'
    WHEN 'CRC' THEN 'img/flags/748045_flag_rica_costa.png'
    WHEN 'HKD' THEN 'img/flags/748046_kong_hong_flag.png'
    WHEN 'XOF' THEN 'img/flags/748047_benin_flag.png'
    WHEN 'PKR' THEN 'img/flags/748051_pakistan_flag.png'
    WHEN 'RON' THEN 'img/flags/748052_flag_romania.png'
    WHEN 'TZS' THEN 'img/flags/748053_flag_tanzania.png'
    WHEN 'DOP' THEN 'img/flags/748054_dominican_republic_flag.png'
    WHEN 'BAM' THEN 'img/flags/748055_flag_bosnia_herzegovina_and.png'
    WHEN 'XAF' THEN 'img/flags/748056_flag_chad.png'
    WHEN 'BRL' THEN 'img/flags/748057_brazil_flag.png'
    WHEN 'XAF' THEN 'img/flags/748058_gabon_flag.png'
    WHEN 'UYU' THEN 'img/flags/748059_flag_uruguay.png'
    WHEN 'ZAR' THEN 'img/flags/748060_africa_flag_south.png'
    WHEN 'XOF' THEN 'img/flags/748061_togo_flag.png'
    WHEN 'BOB' THEN 'img/flags/748062_bolivia_flag.png'
    WHEN 'HUF' THEN 'img/flags/748063_flag_hungary.png'
    WHEN 'SDG' THEN 'img/flags/748064_sudan_flag.png'
    WHEN 'XAF' THEN 'img/flags/748066_flag_cameroon.png'
    WHEN 'SOS' THEN 'img/flags/748069_flag_somalia.png'
    WHEN 'MAD' THEN 'img/flags/748070_morocco_flag.png'
    WHEN 'TWD' THEN 'img/flags/748072_flag_taiwan.png'
    WHEN 'AZN' THEN 'img/flags/748073_azerbaijan_flag.png'
    WHEN 'ETB' THEN 'img/flags/748074_ethiopia_flag.png'
    WHEN 'XCD' THEN 'img/flags/748075_antigua_and_barbuda_flag.png'
    WHEN 'PYG' THEN 'img/flags/748076_paraguay_flag.png'
    WHEN 'AFN' THEN 'img/flags/748077_afghanistan_flag.png'
    WHEN 'IRR' THEN 'img/flags/748079_flag_iran.png'
    WHEN 'BWP' THEN 'img/flags/748080_botswana_flag.png'
    WHEN 'GYD' THEN 'img/flags/748081_guyana_flag.png'
    WHEN 'BYN' THEN 'img/flags/748082_belarus_flag.png'
    WHEN 'UAH' THEN 'img/flags/748083_ukraine_flag.png'
    WHEN 'BDT' THEN 'img/flags/748085_bangladesh_flag.png'
    WHEN 'VES' THEN 'img/flags/748087_flag_venezuela.png'
    WHEN 'ZMW' THEN 'img/flags/748088_flag_zambia.png'
    WHEN 'AOA' THEN 'img/flags/748089_flag_angola.png'
    WHEN 'GMD' THEN 'img/flags/748090_gambia_flag.png'
    WHEN 'GEL' THEN 'img/flags/748092_georgia_flag.png'
    WHEN 'BSD' THEN 'img/flags/748093_thebahamas_flag.png'
    WHEN 'SYP' THEN 'img/flags/748094_flag_syria.png'
    WHEN 'SRD' THEN 'img/flags/748095_suriname_flag.png'
    WHEN 'RWF' THEN 'img/flags/748098_rwanda_flag.png'
    WHEN 'IQD' THEN 'img/flags/748099_flag_iraq.png'
    WHEN 'TND' THEN 'img/flags/748100_tunisia_flag.png'
    WHEN 'HNL' THEN 'img/flags/748101_flag_honduras.png'
    WHEN 'TRY' THEN 'img/flags/748103_flag_turkey.png'
    WHEN 'CLP' THEN 'img/flags/748105_flag_chile.png'
    WHEN 'THB' THEN 'img/flags/748106_flag_thailand.png'
    WHEN 'GHS' THEN 'img/flags/748109_ghana_flag.png'
    WHEN 'COP' THEN 'img/flags/748110_flag_colombia.png'
    WHEN 'RSD' THEN 'img/flags/748111_serbia_flag.png'
    WHEN 'PHP' THEN 'img/flags/748112_philippines_flag.png'
    WHEN 'ILS' THEN 'img/flags/748113_palestine_flag.png'
    WHEN 'PLN' THEN 'img/flags/748114_flag_poland.png'
    WHEN 'GTQ' THEN 'img/flags/748115_flag_guatemala.png'
    WHEN 'JPY' THEN 'img/flags/748116_flag_japan.png'
    WHEN 'SEK' THEN 'img/flags/748117_sweden_flag.png'
    WHEN 'NZD' THEN 'img/flags/748118_flag_new_zealand.png'
    WHEN 'JMD' THEN 'img/flags/748119_jamaica_flag.png'
    WHEN 'LBP' THEN 'img/flags/748121_flag_lebanon.png'
    WHEN 'PEN' THEN 'img/flags/748122_peru_flag.png'
    WHEN 'CHF' THEN 'img/flags/748124_flag_switzerland.png'
    WHEN 'SGD' THEN 'img/flags/748125_singapore_flag.png'
    WHEN 'MZN' THEN 'img/flags/748127_flag_mozambique.png'
    WHEN 'GNF' THEN 'img/flags/748129_guinea_flag.png'
    WHEN 'NOK' THEN 'img/flags/748131_norway_flag.png'
    WHEN 'INR' THEN 'img/flags/748132_india_flag.png'
    WHEN 'VND' THEN 'img/flags/748133_flag_vietnam.png'
    WHEN 'JOD' THEN 'img/flags/748134_jordan_flag.png'
    WHEN 'IDR' THEN 'img/flags/748135_flag_indonesia.png'
    WHEN 'LRD' THEN 'img/flags/748136_liberia_flag.png'
    WHEN 'MXN' THEN 'img/flags/748137_mexico_flag.png'
    WHEN 'YER' THEN 'img/flags/748138_yemen_flag.png'
    WHEN 'NGN' THEN 'img/flags/748140_flag_nigeria.png'
    WHEN 'NIO' THEN 'img/flags/748141_nicaragua_flag.png'
    WHEN 'ZWL' THEN 'img/flags/748142_flag_zimbabwe.png'
    ELSE 'img/default_flag.png'
END