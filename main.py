from templates import columns, sheet
from product import CreateProduct

if __name__ == '__main__':
    product = CreateProduct(columns, sheet)
    product.create_empty_df()
    product.read_csv()
    product.ready_list()
    product.fill_df()
