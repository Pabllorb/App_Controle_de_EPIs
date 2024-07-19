import xml.etree.ElementTree as ET


def gerar_relatorio_entregas(entregas, file_path):
    root = ET.Element("Entregas")

    for entrega in entregas:
        entrega_elem = ET.SubElement(root, "Entrega")

        id_elem = ET.SubElement(entrega_elem, "ID")
        id_elem.text = str(entrega[0])

        epi_id_elem = ET.SubElement(entrega_elem, "EPI_ID")
        epi_id_elem.text = str(entrega[1])

        nome_epi_elem = ET.SubElement(entrega_elem, "Nome_EPI")
        nome_epi_elem.text = entrega[2]

        nome_epi_elem = ET.SubElement(entrega_elem, "Descrição_EPI")
        nome_epi_elem.text = entrega[3]

        data_entrega_elem = ET.SubElement(entrega_elem, "Data_Entrega")
        data_entrega_elem.text = entrega[4]

        setor_elem = ET.SubElement(entrega_elem, "Setor")
        setor_elem.text = entrega[5]

        quantidade_elem = ET.SubElement(entrega_elem, "Quantidade")
        quantidade_elem.text = str(entrega[6])

    tree = ET.ElementTree(root)
    tree.write(file_path, encoding='utf-8', xml_declaration=True)


def gerar_relatorio_epis(epis, file_path):
    root = ET.Element("EPIs")

    for epi in epis:
        epi_elem = ET.SubElement(root, "EPI")

        id_elem = ET.SubElement(epi_elem, "ID")
        id_elem.text = str(epi[0])

        nome_elem = ET.SubElement(epi_elem, "Nome")
        nome_elem.text = epi[1]

        descricao_elem = ET.SubElement(epi_elem, "Descricao")
        descricao_elem.text = epi[2]

        marca_elem = ET.SubElement(epi_elem, "Marca")
        marca_elem.text = epi[3]

        ca_elem = ET.SubElement(epi_elem, "CA")
        ca_elem.text = str(epi[4])

        validade_elem = ET.SubElement(epi_elem, "Validade")
        validade_elem.text = epi[5]

        unidade_elem = ET.SubElement(epi_elem, "Unidade")
        unidade_elem.text = str(epi[6])

        quantidade_elem = ET.SubElement(epi_elem, "Quantidade")
        quantidade_elem.text = str(epi[7])

        imagem_elem = ET.SubElement(epi_elem, "Imagem")
        imagem_elem.text = epi[8]

    tree = ET.ElementTree(root)
    tree.write(file_path, encoding='utf-8', xml_declaration=True)
