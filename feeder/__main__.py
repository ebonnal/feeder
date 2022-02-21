import time
import sys
from pynput.mouse import Button, Controller

class ClicPoint:

    mouse = Controller()

    def __init__(self, coords, actions_delay_seconds = 1):
        self.coords = coords
        self.actions_delay_seconds = actions_delay_seconds
    
    def delay(self):
        time.sleep(self.actions_delay_seconds)

    def point_at(self):
        self.mouse.position = self.coords
        self.delay()

    def clic(self):
       self.point_at()
       self.mouse.click(Button.left, 1)
       self.delay()
       
    def double_clic(self):
       self.point_at()
       self.mouse.click(Button.left, 2)
       self.delay()

    def drag_and_drop(self, target_point):
       self.point_at()
       self.mouse.press(Button.left)
       self.delay()
       target_point.point_at()
       self.mouse.release(Button.left)
       self.delay()

class Coords:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def minus(self, coords):
        return Coords(self.x - coords.x, self.y - coords.y)
    
    def plus(self, coords):
        return Coords(self.x + coords.x, self.y + coords.y)
    
    def times(self, scalar):
        return Coords(scalar * self.x, scalar * self.y)

class ClicPointFactory:
    ref_origin = Coords(209.46170043945312, 55.83537292480469)

    ref_fami_slot_relative_coords = Coords(945.1976318359375, 284.1272888183594).minus(ref_origin)
    ref_equip_tab_relative_coords = Coords(1058.3575439453125, 184).minus(ref_origin)
    ref_resou_tab_relative_coords = Coords(1118.3980712890625, 184).minus(ref_origin)
    ref_first_inv_slot_relative_coords = Coords(1031.5552978515625, 278.10980224609375).minus(ref_origin)

    ref_tabs_x_diff = ref_resou_tab_relative_coords.x - ref_equip_tab_relative_coords.x

    ref_inv_slot_width = 1097.438720703125 - 1055.46826171875
    ref_inv_slot_height = 340.6443786621094 - 299.8241271972656

    def __init__(self, equip_tab_x_coord, resou_tab_x_coord):
        if equip_tab_x_coord is None or resou_tab_x_coord is None:
            self.coef = 1  # TODO remove, dev only
        else:
            self.coef = (resou_tab_x_coord - equip_tab_x_coord) / self.ref_tabs_x_diff
        self.origin = equip_tab_x_coord.minus(self.ref_equip_tab_relative_coords.times(self.coef))
    
    def __init__(self, equip_tab_x_coord, resou_tab_x_coord):
        self.coef = (resou_tab_x_coord - equip_tab_x_coord) / self.ref_tabs_x_diff
        self.origin = equip_tab_x_coord.minus(self.ref_equip_tab_relative_coords.times(self.coef))
    
    def _true_coords_from_ref(self, coords):
        coords.times(self.coef).plus(self.origin)

    def createFamiInvSlots(self, n_famis):
        return [
            ClicPoint(
                self._true_coords_from_ref(self.ref_first_inv_slot_relative_coords)
                .plus(
                    Coords(
                        self.ref_inv_slot_width * self.coef * (i % 4),
                        self.ref_inv_slot_height * self.coef * (i // 4)
                    )
                )
            )
            for i in range(n_famis)
        ]
    
    def createEquipmentTab(self):
        return ClicPoint(self._true_coords_from_ref(self.ref_equip_tab_relative_coords))

    def createResourcesTab(self):
        return ClicPoint(self._true_coords_from_ref(self.ref_resou_tab_relative_coords))
    
    def createFamiSlot(self):
        return ClicPoint(self._true_coords_from_ref(self.ref_fami_slot_relative_coords))

    def createFoodInvSlot(self):
        return ClicPoint(self._true_coords_from_ref(self.ref_first_inv_slot_relative_coords))

class FeedStrategy:
    def __init__(self, clic_point_factory: ClicPointFactory, n_famis: int):
        self.fami_inv_slots: iter[ClicPoint] = clic_point_factory.createFamiInvSlots(n_famis)
        self.equip_tab: ClicPoint = clic_point_factory.createEquipmentTab()
        self.res_tab: ClicPoint = clic_point_factory.createResourcesTab()
        self.fami_slot: ClicPoint = clic_point_factory.createFamiSlot()
        self.food_inv_slot: ClicPoint = clic_point_factory.createFoodInvSlot()

    def feed(self):
        self.equip_tab.clic()
        self.fami_inv_slots[0].double_clic()
        self.res_tab.clic()
        self.food_inv_slot.drag_and_drop(self.fami_slot)
        for fami_inv_slot in self.fami_inv_slots[:-1]:
            self.equip_tab.clic()
            fami_inv_slot.double_clic()
            self.res_tab.clic()
            self.food_inv_slot.drag_and_drop(self.fami_slot)

class Main:
    def run(feed_strategy: FeedStrategy):
        time.sleep(3)
        feed_strat.feed()


if __name__ == "__main__":
    clic_point_factory = ClicPointFactory(None, None)
    feed_strat = FeedStrategy(clic_point_factory, int(sys.argv[1]))
    Main.run(feed_strat)