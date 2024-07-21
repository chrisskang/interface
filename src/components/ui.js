import { Pane } from "tweakpane";

export const ui = new Pane({title: 'Parameters'});

const f1 = ui.addFolder({
  title: 'joint 1',
});
f1.addBlade({
  view: 'slider',
  label: 'joint 1',
  min: -30,
  max: 30,
  value: 0.5,
});
f1.addBinding({
  active: true,
}, 'active');

const f2 = ui.addFolder({
  title: 'joint 2',
});
f2.addBlade({
  view: 'slider',
  label: 'joint 2',
  min: -30,
  max: 30,
  value: 0.5,
});
f2.addBinding({
  active: true,
}, 'active');

const f3 = ui.addFolder({
  title: 'joint 3',
});
f3.addBlade({
  view: 'slider',
  label: 'joint 3',
  min: -30,
  max: 30,
  value: 0.5,
});
f3.addBinding({
  active: true,
}, 'active');

const f4 = ui.addFolder({
  title: 'joint 4',
});
f4.addBlade({
  view: 'slider',
  label: 'joint 4',
  min: -30,
  max: 30,
  value: 0.5,
});
f4.addBinding({
  active: true,
}, 'active');

const f5 = ui.addFolder({
  title: 'joint 5',
});
f5.addBlade({
  view: 'slider',
  label: 'joint 5',
  min: -30,
  max: 30,
  value: 0.5,
});
f5.addBinding({
  active: true,
}, 'active');

const PARAMS = {
  wave: "hi",
};

ui.addBinding(PARAMS, 'wave', {
  readonly: true,
  multiline: true,
  rows: 5,
});
ui.addButton({
  title: 'full send',
  label: 'execute',   // optional
});