import re

# ###################################################### 电话 ######################################################## #
phone_rule_names = ["one_label", "double_labels"]


def one_label(text):
    text_one = re.sub('&nbsp;', '', text)
    phones = re.findall('电 *话[号]?[码]? *[:：] *<.*?>[( )+\d-]{10,}|'
                        '手 *机 *[:：] *<.*?>[( )+\d-]{10,}|'
                        '热 *线 *[:：] *<.*?>[( )+\d-]{10,}|'
                        '直 *线 *[:：] *<.*?>[( )+\d-]{10,}|'
                        'Tel *[:：] *<.*?>[( )+\d-]{10,}', text_one)
    result = []
    for phone in phones:
        result.append(re.sub('<.*?>', '', phone))
    return result


def double_labels(text):
    phones = re.findall('电[ \u3000]*话[号]?[码]? *[:：] *</.*?>[\s\S]*<.*?>[( )+\d-]{10,}|'
                        '手[ \u3000]*机 *[:：] *</.*?>[\s\S]*<.*?>[( )+/\d-]{10,}|'
                        '热[ \u3000]*线 *[:：] *</.*?>[\s\S]*<.*?>[( )+/\d-]{10,}|'
                        '直[ \u3000]*线 *[:：] *</.*?>[\s\S]*<.*?>[( )+/\d-]{10,}|'
                        'Tel *[:：] *</.*?>[\s\S]*<.*?>[( )+\d-]{10,}', text)
    result = []
    for phone in phones:
        result.append(re.sub('<.*?>|\u3000|\r|\n|/', '', phone))
    return result


# ####################################################### QQ ######################################################### #
qq_rule_names = ['qq_wake', 'qq_label', 'qq_nbsp']


def qq_wake(text):
    result = []
    wake_qqs = re.findall('[Uu]in=\d{7,}', text)
    for wake_qq in wake_qqs:
        if re.findall('\d+', wake_qq):
            result.append("QQ：" + wake_qq[4:])
    return result


def qq_label(text):
    result = []
    rule_qqs = re.findall('[Qq] *[Qq] *<.*?><.*?> *[:：] *<.*?><.*?>(.*?)<.*?>', text)
    for rule_qq in rule_qqs:
        result.append(rule_qq.replace('&nbsp;', ''))
    return result


def qq_nbsp(text):
    result = []
    text = text.replace('&nbsp;', '')
    nbsp_qqs = re.findall('[Qq] *[Qq] *[:：]?\d{7,}', text)
    for nbsp_qq in nbsp_qqs:
        if ':' not in nbsp_qq and '：' not in nbsp_qq:
            chips = re.findall('\d+', nbsp_qq)
            if len(chips) != 0:
                result.append('QQ：' + chips[0])
        else:
            result.append(nbsp_qq)
    return result
