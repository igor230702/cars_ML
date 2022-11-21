# Предсказывание стоимости автомобиля

## Описание проекта
Когда я думал над идеей для своего проекта, одной из первых мне в голову пришла мысль предсказывать стоимость какого-либо товара в зависимости от его признаков. Сначала я хотел выбрать что-то, с чем часто имею дело в повседневной жизни, однако вскоре переключился на категорию автомобилей. У них множество признаков, причём от машины к машине их перечень практически не меняется - датасет получился бы очень удобным. Может, я и не смогу использовать эту модель по назначению, однако автомобилистам она явно может пригодиться.

В процессе исслеования я буду использовать данные, обладающие следующими признаками:
*   engine: объём двигателя
*   power: мощность в л. с.
*   transmission: тип коробки передач
*   drive_unit: тип привода
*   body_type: тип кузова
*   color: цвет
*   mileage: пробег
*   steering_wheel: руль (с какой стороны он находится)
*   gen: поколение автомобиля
*   equipment: комплектация
*   price: цена автомобиля

## Содержание проекта

1. **Парсинг**. Я написал свой персер на python для сайта https://auto.drom.ru/. Возникла проблема с тем, что сайт не позволял спарсить больше 100 страниц, поэтому пока мой датасет ограничивается лишь 2000 строк. Позже я подумаю, как можно обойти это ограничение.
2. **Обработка данных**. 
Данные получились достаточно грязными - в них много пропусков, а один признак вообще имеет меньше половины непустых значений. На первых порах я решил удалить этот полупустой признак и дропнуть остальные NaN'ы. В итоге из 2000 объектов осталось ~1600. 
3. **Обучение моделей**.
4. **Сравнение моделей**.
