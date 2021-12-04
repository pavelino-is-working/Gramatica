import json
from automatFinit import AutomatFinit

class Gramatica:
    def __init__(self, neterminale, terminale, productii, initial):
        self.neterminale = list(neterminale)
        self.terminale = terminale
        self.productii = productii
        self.initial = initial

    @staticmethod
    def pretty_productie_form(productie):
        pretty_productie = ""
        pretty_productie += f"{productie[0]} ->"
        for elem in productie[1]:
            pretty_productie += f" {elem} |"
        return pretty_productie

    def __str__(self):
        print_productii = ""
        for productie in self.productii:
            print_productii += "\t" + self.pretty_productie_form(productie) + "\n"
        return f"Simboluri neterminale: {self.neterminale} \n" \
               f"Simboluri terminale {self.terminale} \n" \
               f"Productii \n{print_productii}" \
               f"Simbol initial {self.initial}"

    def verificare_sintaxa(self, drumuri):
        for drum in drumuri:
            if 0 < len(drum) < 3:
                if len(drum) == 1:
                    if drum not in self.terminale:
                        return False
                elif drum[0] not in self.terminale or drum[1] not in self.neterminale:
                    return False
            else:
                return False
        return True

    def verificare_regularitate(self):
        """
        Verifica regularitatea automatului
        :return: True daca este Gramatica regulara, False altfel
        """
        for productie in self.productii:
            if (len(productie[0]) != 1 and productie[0] not in self.neterminale) or\
                    not self.verificare_sintaxa(productie[1]):
                print(f"Nu este Gramatica regulara")
                return False
            return True

    def producti_in_tranziti(self):
        """
        Transforma productile gramatici regulare in tranziti pentru automatul finit
        """
        tranziti = {}
        for productie in self.productii:

            for elem in productie[1]:
                tranzitie = None
                if len(elem) == 2:
                    if (productie[0],elem[0]) not in tranziti:
                        tranziti[(productie[0],elem[0])] = [elem[1]]
                    else:
                        my_tranzitie = tranziti[(productie[0],elem[0])]
                        my_tranzitie.append(elem[1])
                        tranziti[(productie[0],elem[0])] = my_tranzitie
                else:
                    if (productie[0], elem[0]) not in tranziti:
                        tranziti[(productie[0], elem[0])] = ["K"]
                    else:
                        my_tranzitie = tranziti[(productie[0],elem[0])]
                        my_tranzitie.append("K")
                        tranziti[(productie[0], elem[0])] = my_tranzitie
        my_tranziti = []
        for key, value in tranziti.items():
            my_tranziti.append([key[0], key[1], value])
        return my_tranziti

    def conversie_gr_af(self):
        """
        Transforma o gramatica regulara intr-un automat finit :D
        """
        # verifica daca gramatica este regulara
        if self.verificare_regularitate():
            my_list = self.neterminale
            my_list.append("K")
            automat_finit = {"stari_finale": ["K"], "stari": my_list,
                             "stare_initiala": self.initial, "alfabet": self.terminale,
                             "tranziti": self.producti_in_tranziti()}
            with open("gr_in_af.json", "w") as file:
                json.dump(automat_finit, file)
        else:
            print("Nu se poate face conversia pentru ca Gramatica NU ESTE regulara")


def main():
    with open("gramatica.json") as f:
        data = dict(json.load(f))

    gramatica = Gramatica(data["neterminale"], data["terminale"], data["productii"], data["initial"])
    print(gramatica, '\n')
    gramatica.conversie_gr_af()

    with open("gr_in_af.json") as f:
        data = dict(json.load(f))

    af = AutomatFinit(data['stari'], data['alfabet'], data['tranziti'],
                      data['stare_initiala'], data['stari_finale'])

    af.print_automat()
    af.conversie_af_gr()

    with open("af_in_gr.json") as f:
        data = dict(json.load(f))

    gramatica2 = Gramatica(data["neterminale"], data["terminale"], data["productii"], data["initial"])
    print(gramatica2, "\n")


if __name__ == '__main__':
    main()
