from collections import OrderedDict


class ThingRecipe():
    def __init__(self, name, time_to_produce=None, amount_produced=None, components={}):
        self.name = name
        if self.name in components:
            raise Exception('Component cannot be made of itself.')
        assert all(isinstance(c, ThingRecipe) for c in components)
        self.components = components
        self.time_to_produce = time_to_produce
        self.amount_produced = amount_produced
        self.base_units = self._resolve()
        if len(self.components) > 0:
            self.per_min_mult = self.amount_produced / self.time_to_produce * 60

    def _resolve(self):
        if len(self.components) == 0:
            return {self: 1}

        base_units = {}
        for component, amount in self.components.items():
            component_base_units = component.base_units
            for base_component, base_amount in component_base_units.items():
                base_units.setdefault(base_component, 0)
                base_units[base_component] += (amount / self.amount_produced) * base_amount

        base_units = OrderedDict(sorted(base_units.items(), key=lambda x: x[1], reverse=True))
        return base_units

    def __str__(self):
        if len(self.components) == 0:
            return self.name
        per_base_unit = ', '.join(f'{k}: {v:g}' for k,v in self.base_units.items())
        per_min = ', '.join(f'{v*self.per_min_mult:g} {k}/min' for k,v in self.base_units.items())
        output = f'{self.name}'
        output += f'  ({per_base_unit})'
        output += f'  [{per_min}]'
        return output

    def __repr__(self):
        return f'<{self.__class__.__name__}: {str(self)}>'

class ThingPerMin(ThingRecipe):
    def __init__(self, name, amount_produced_per_min=None, components_per_min={}):
        time_to_produce = 1 / amount_produced_per_min * 60
        components = {}
        for k,v in components_per_min.items():
            components[k] = v / 60 * time_to_produce
        super(ThingPerMin, self).__init__(name, time_to_produce, 1, components)



# ThingRecipe('name', seconds_to_produce, amount_produced, {ingredients: count})
# ThingPerMin('name', amount_produced_per_min, {ingredients: count_per_min})

iron_ore = ThingRecipe('iron')
iron_ingot = ThingRecipe('iron-ingot', 2, 1, {iron_ore: 1})
iron_plate = ThingRecipe('iron-plate', 6, 2, {iron_ingot: 3})
iron_rod = ThingRecipe('iron-rod', 4, 1, {iron_ingot: 1})
screw = ThingRecipe('screw', 6, 4, {iron_rod: 1})
reinforced_plate = ThingRecipe('reinforced-plate', 12, 1, {iron_plate: 6, screw: 12})
rotor = ThingRecipe('rotor', 15, 1, {iron_rod: 5, screw: 25})
smart_plating = ThingRecipe('smart-plating', 30, 1, {reinforced_plate: 1, rotor: 1})
modular_frame = ThingRecipe('modular-frame', 60, 2, {reinforced_plate: 3, iron_rod: 12})

copper_ore = ThingRecipe('copper')
copper_ingot = ThingRecipe('copper-ingot', 2, 1, {copper_ore: 1})
wire = ThingRecipe('wire', 4, 2, {copper_ingot: 1})
copper_sheet = ThingRecipe('copper-sheet', 6, 1, {copper_ingot: 2})
cable = ThingRecipe('cable', 2, 1, {wire: 2})

limestone = ThingRecipe('limestone')
concrete = ThingRecipe('concrete', 4, 1, {limestone: 3})

coal = ThingRecipe('coal')
steel_ingot = ThingRecipe('steel-ingot', 4, 3, {iron_ore: 3, coal: 3})
steel_beam = ThingRecipe('steel-beam', 4, 1, {steel_ingot: 4})
steel_pipe = ThingRecipe('steel-pipe', 6, 2, {steel_ingot: 3})
encased_industrial_beam = ThingRecipe('encased-steel-beam', 10, 1, {steel_beam: 4, concrete: 5})

versatile_framework = ThingRecipe('versatile-framework', 24, 2, {modular_frame: 1, steel_beam: 12})
stator = ThingRecipe('stator', 12, 1, {steel_pipe: 3, wire: 8})
automated_wiring = ThingRecipe('automated-wiring', 24, 1, {stator: 1, cable: 20})

caterium_ore = ThingRecipe('caterium')
caterium_ingot = ThingRecipe('caterium-ingot', 4, 1, {caterium_ore: 3})
quickwire = ThingRecipe('quickwire', 5, 5, {caterium_ingot: 1})

ai_limiter = ThingRecipe('ai-limiter', 12, 1, {quickwire: 20, copper_sheet: 5})

motor = ThingRecipe('motor', 12, 1, {stator: 2, rotor: 2})

plastic = ThingRecipe('plastic')
circuit_board = ThingRecipe('circuit-board', 8, 1, {copper_sheet: 2, plastic: 4})
computer = ThingRecipe('computer', 24, 1, {circuit_board: 10, cable: 9, plastic: 18, screw: 52})
high_speed_connector = ThingRecipe('high-speed-connector', 16, 1, {circuit_board: 1, cable: 10, quickwire: 56})

heavy_modular_frame = ThingRecipe('heavy-modular-frame', 30, 1, {modular_frame: 5, steel_pipe: 15, encased_industrial_beam: 5, screw: 100})
adaptive_control_unit = ThingPerMin('adaptive-control-unit', 1, {automated_wiring: 7.5, circuit_board: 5, heavy_modular_frame: 1, computer: 1})



grouped_things = {}

for var in dict(locals()).values():
    if isinstance(var, ThingRecipe):
        if len(var.components) > 0:
            group = next(iter(var.base_units))
            if group not in grouped_things:
                grouped_things[group] = []
            grouped_things[group].append(var)

for k,v in grouped_things.items():
    print('\n%s tower:' % k)
    print('\n'.join(str(x) for x in v))
