from lxml import etree
import argparse

NAMESPACES = {'x':'http://opcfoundation.org/UA/2011/03/UANodeSet.xsd'}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("reference")
    parser.add_argument("test")

    args = parser.parse_args()
    print(args.reference)

    reference_f = open(args.reference, 'r', encoding='utf-8')
    reference_tree = etree.parse(reference_f)

    for ref_object in reference_tree.xpath('x:UAObject', namespaces=NAMESPACES):
        print(ref_object)

if __name__ == "__main__":
    main()
