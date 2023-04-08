class JSON:
    @staticmethod
    def create_object(data):
        obj = dict(zip(data.columns, data.values[0]))
        return obj

    def create_result_object(self,  num_data, cat_data, normalize_num_data, normalize_cat_data, result):
        num_dict = self.create_object(num_data)
        cat_dict = self.create_object(cat_data)
        norm_num_dict = self.create_object(normalize_num_data)
        norm_cat_dict = self.create_object(normalize_cat_data)
        revenue_dict = {'revenue': result[0]}

        result_object = {'num_data': num_dict, 'cat_data': cat_dict, 'normalize_num_data': norm_num_dict,
                         'normalize_cat_data': norm_cat_dict, 'revenue': revenue_dict}

        return result_object
