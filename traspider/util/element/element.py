from lxml import etree

from traspider.util.traerror import ElementError


class Element():
    def __init__(self, element):
        self.element = element

    def extract(self):
        if isinstance(self.element, list):
            print(self.element)
            self.element = [element
                            if isinstance(element, str) else etree.tostring(
                element,
                method="html",
                encoding="unicode",
                with_tail=False
            ) for element in self.element]
        return self.element

    def extract_first(self):
        if isinstance(self.element, list) and len(self.element) > 0:
            # 如果self.element中第一位是字符串的话直接返回,否则将element对象转换为字符串
            return self.element[0] if isinstance(self.element[0], str) else etree.tostring(
                self.element[0],
                method="html",
                encoding="unicode",
                with_tail=False
            )
        if isinstance(self.element, str):
            return self.element
        raise ElementError("<element length is 0>")

    def get_index(self, index):
        if isinstance(self.element, list) and len(self.element) > 0:
            return self.element[index]
        if isinstance(self.element, str):
            raise ElementError("<Use get_index for strings>")
        raise ElementError("<element length is 0>")

    def xpath(self, query):
        xpath_list = self.element.xpath(query)
        if isinstance(xpath_list, list):
            return ElementIter(xpath_list)
        return Element(xpath_list)


class ElementIter(Element):

    def __init__(self, element):
        self.element = element

    def __iter__(self):
        for element in self.element:
            yield Element(element)

    def __repr__(self):
        return str(self.element)
