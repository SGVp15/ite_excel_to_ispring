def compress(list_a: list, list_max: list, num) -> (list, list):
    size = sum(list_a)
    if sum(list_a) <= num:
        return list_a, list_max
    else:
        data = _get_list_dict(list_a, list_max)
        # Сортируем по максимальному вхождению и проценту вхождения
        # data.sort(key=lambda x: (x['proc'], x['max_value']), reverse=True)
        data.sort(key=lambda x: (x['proc'], x['max_value']), reverse=True)

        for i, dict_ in enumerate(data):
            if dict_['value'] == 1:
                continue
            dict_['value'] -= 1
            break
        data.sort(key=lambda x: (x['index']))
        for i, dict_ in enumerate(data):
            list_a[i] = dict_['value']
        return (compress(list_a, list_max, num))


def _get_list_dict(list_a: list, list_max: list):
    data = []
    for i in range(len(list_max)):
        data.append({
            'index': i,
            'value': list_a[i],
            'max_value': list_max[i],
            'proc': (list_a[i] - 2) / list_max[i],
        })
    return data
