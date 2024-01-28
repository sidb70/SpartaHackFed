import torch
from models.loan_defaulter import LoanDefaulterModel, get_loan_defaulter_data
import io


if __name__ == '__main__':
    # load state_dict from model.pth

    try:
        with open('model.pth', 'rb') as f:
            file = io.BytesIO(f.read())
    except FileNotFoundError:
        file = None

    node_hash = 1   
    model = LoanDefaulterModel(get_loan_defaulter_data(node_hash), file)
    result = model.train()
    # model.evaluate(result)
    torch.save(result, 'model.pth')
