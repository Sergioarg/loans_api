@test
def test_get_available_amount():
    # Arrage
    score = 1000
    total_debt = 500
    # Act
    result = get_available_amount(score, total_debt)
    # Result
    assert (result, 500)

def test_get_available_amount_negatives():
    # Arrage
    score = -1000
    total_debt = 500
    # Act
    result = get_available_amount(score, total_debt)

    # Result
    # TODO: Test con excepcion
    assert (result, -500)

def test_get_available_amount_strings():
    # Arrage
    score = -1000
    total_debt = 500
    # Act
    result = get_available_amount(score, total_debt)

    # Result
    # TODO: Test con excepcion
    assert (result, -500)


def test_get_available_amount_zero():
    # Arrage
    score = 1000
    total_debt = 1000
    # Act
    result = get_available_amount(score, total_debt)

    # Result
    # TODO: Test con excepcion
    assert (result, -500)

def test_get_outstandings():
    # 1. Recibe un customer
    # 2. Obtiene el Id

    # 3. Hace una consulta en BD de los loans
    # ---------------------------------
    # 4.
    loan1 = Loan(1000, 'external_id')
    loan2 = Loan(2000, 'external_id')
    loan3 = Loan(3000, 'external_id')
    loans = [loan, loan, loan]


    outstanding = get_total_outstanding(loans)

    assert (outstanding, 6000)


def test_customer():
    # TEST: Que va a la vista
    
    pass
