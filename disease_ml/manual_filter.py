class ManualFilter:
    def __init__(self):
        self.filters = ['sniff', 'sneeze', 'bleed', 'blood', 'why']
    def runFilter(self, input_list, output_list):
        for filter in self.filters:
            if filter in input_list:
                output_list.append(filter)
        return output_list

#x = ManualFilter()
#output_list = []
#output_list = x.runFilter(['sniff', 'blood'], output_list)
#print output_list
