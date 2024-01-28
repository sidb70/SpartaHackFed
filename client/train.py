import torch
from models.loan_defaulter import LoanDefaulterModel, get_loan_defaulter_data



if __name__ == '__main__':
    # load state_dict from model.pth
    try:
        state_dict = torch.load('model.pth')
    except FileNotFoundError:
        state_dict = None

    node_hash = 1   
    model = LoanDefaulterModel(get_loan_defaulter_data(node_hash), state_dict)
    result = model.train()
    # model.evaluate(result)
    torch.save(result, 'model.pth')
