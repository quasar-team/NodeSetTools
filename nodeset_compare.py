#!/usr/bin/env python3

from lxml import etree
import argparse
import pdb
import sys
import logging

from colorama import Fore, Style

NAMESPACES = {'x':'http://opcfoundation.org/UA/2011/03/UANodeSet.xsd'}

def etree_from_filename(fn):
    file = open(fn, 'r', encoding='utf-8')
    return etree.parse(file)

def nodeid_scan(entity_type, reference_tree, test_tree, ignore_nodeids):
    '''Scans all entity_type in reference tree and xvalidates in test_tree
    entity_type to be anything that has NodeId, so any descendant of UANode, e.g. UAVariable, UAObject...'''
    any_failure = False
    for ref_entity in reference_tree.xpath(f'x:{entity_type}', namespaces=NAMESPACES):
        ref_nodeid = ref_entity.attrib["NodeId"]
        if any([id in ref_nodeid for id in ignore_nodeids]):
            print(f'{Fore.YELLOW}Ignoring{Style.RESET_ALL} the entity with nodeid: {Fore.BLUE}{ref_nodeid}{Style.RESET_ALL}')
            continue
        logging.debug(f'At: {ref_nodeid}')
        xpath_expr = f"x:{entity_type}[@NodeId='{ref_nodeid}']"
        q = test_tree.xpath(xpath_expr, namespaces=NAMESPACES)
        if len(q) != 1:
            print(f'Error: entity in test_tree. Type: {entity_type}, NodeId: {ref_nodeid}')
            any_failure = True
        test_element = q[0]
        if test_element != ref_entity:
            # let's see why they are different.
            if test_element.attrib != ref_entity.attrib:
                for attr in ref_entity.attrib:
                    try:
                        if test_element.attrib[attr] != ref_entity.attrib[attr]:
                            print(f"reference attribute value fail, attribute{attr} ref_value{ref_entity.attrib[attr]} test_value{test_element.attrib[attr]}")
                            any_failure = True
                    except KeyError:
                        print(f'{Fore.RED}Attribute {Fore.YELLOW}{attr}{Fore.RED} is missing in test entity{Style.RESET_ALL}(at nodeid: {ref_nodeid})')
                        any_failure = True
            #pdb.set_trace()
    return any_failure


def main():
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument("reference")
    parser.add_argument("test")
    parser.add_argument("--ignore_nodeids", nargs="*", default=[])

    args = parser.parse_args()
    print(args.reference)

    reference_tree = etree_from_filename(args.reference)
    test_tree = etree_from_filename(args.test)

    any_failure = False

    NodeIdEntities = ['UAObject', 'UAVariable', 'UAMethod']
    for entity_type in NodeIdEntities:
        fail = nodeid_scan(entity_type, reference_tree, test_tree, args.ignore_nodeids)
        any_failure = any_failure or fail

    if any_failure:
        sys.exit(1)


if __name__ == "__main__":
    main()
