# -*- coding: utf-8 -*-
# Created by apple on 2018/6/27.

import os


class BrewPackage:
    def __init__(self, name: str):
        self.name = name
        self.deps = []
        self.is_dep = False

    @classmethod
    def _deps_str(cls, package, level: int = 0, need_deep: bool = True):
        ts = '\t' * (level + 1)
        s = ''
        for p in package.deps:
            s += '{}- {}\n'.format(ts, p.name)
            if need_deep and p.deps:
                s += cls._deps_str(p, level + 1)
        return s

    def __repr__(self) -> str:
        return '{}:\n{}'.format(self.name, BrewPackage._deps_str(self))


all_package_dict = {}  # name -> package


def get_cache_package(package_name: str) -> BrewPackage:
    pkg = all_package_dict.get(package_name)
    if not pkg:
        pkg = BrewPackage(package_name)
        all_package_dict[package_name] = pkg
    return pkg


with os.popen('brew deps --installed') as popen:
    dep_lines = popen.read().split('\n')

    for line in dep_lines:
        if not line:
            continue

        result = line.split(': ')
        name = result[0]
        deps_name = result[1].split(' ') if len(result) == 2 and result[1] else None

        package = get_cache_package(name)

        if not deps_name:
            continue
        for dep_name in deps_name:
            dep_package = get_cache_package(dep_name)
            dep_package.is_dep = True
            package.deps.append(dep_package)

    print('All package and deps')
    print('--------------------')
    for package in all_package_dict:
        print(package)
    print('\n')

    print('Not dependent packages')
    print('----------------------')
    not_dep_package = [p for p in all_package_dict.values() if not p.is_dep]
    for p in not_dep_package:
        print(p.name)

