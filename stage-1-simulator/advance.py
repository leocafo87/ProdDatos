import sys

import simulator

if __name__ == "__main__":
    if len(sys.argv) == 1:
        #Se ejecuta el primer lote
        print('Se procesa un solo lote')
        batch_list = ['1']
        simulator.process_next_batches(batch_list)
    else:
        #Se ejecutan los lotes que se indiquen
        response = (sys.argv[1])
        print('los lotes {} seran procesados '.format(str(response)))
        #Convertir a lista
        batch_list = list(map(int, response.split(',')))
        simulator.process_next_batches(batch_list)
