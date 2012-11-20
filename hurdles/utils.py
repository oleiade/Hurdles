# -*- coding: utf-8 -*-


def average(collection):
    return sum(collection) / len(collection)


def median(collection):
    sorts = sorted(collection)
    length = len(sorts)

    if not length % 2:
        return (sorts[length / 2] + sorts[length / 2 - 1]) / 2

    return sorts[length / 2]
