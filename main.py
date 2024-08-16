from multiprocessing import Process, Manager


class WarehouseManager:
    def __init__(self):
        self.data = Manager().dict()

    def process_request(self, requests):  # запрос
        product, report, quantity = requests  # продукт, отчет, количество в кортеже
        if report == 'receipt':  # получение
            if product in self.data:  # если продукт в данных то
                self.data[product] += quantity  # если продукт в наличии, то + количество
            else:
                self.data[product] = quantity  # если нет в наличии, то вносим количество
        elif report == 'shipment':  # отгрузка
            if self.data[product] >= quantity:  # продукт >= количество
                self.data[product] -= quantity  # продукт -= количество

    def run(self, requests):
        processes = []
        for request in requests:
            ps = Process(target=self.process_request, args=(request,))
            processes.append(ps)
            ps.start()
        for ps in processes:
            ps.join()


if __name__ == '__main__':
    manager = WarehouseManager()
    requests = [("product1", "receipt", 100),
                ("product2", "receipt", 150),
                ("product1", "shipment", 30),
                ("product3", "receipt", 200),
                ("product2", "shipment", 50),
                ("product2", "shipment", 100)]

    manager.run(requests)
    print(manager.data)

