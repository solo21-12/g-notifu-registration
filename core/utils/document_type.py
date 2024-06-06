class DocumentType:
    THIRD_PARTY_INSURANCE = 'Third party insurance'
    ROAD_FUND = 'Road fund'
    ROAD_AUTHORITY = 'Road Authority'
    BOLO = 'Bolo'

    document_type_choices = [
        (THIRD_PARTY_INSURANCE, 'Third party insurance'),
        (ROAD_FUND, 'Road Fund'),
        (ROAD_AUTHORITY, 'Road Authority'),
        (BOLO, 'Bolo')
    ]
