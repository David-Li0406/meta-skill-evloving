import { East, StringType } from "@elaraai/east";
import * as e3 from "@elaraai/e3";
import { MyStringType } from "./types.js";

const example = e3.customTask(
  "main",
  [],
  StringType,
  (inputs, output) => East.value(`Hello`, MyStringType)
);

export default e3.package('example', '1.1.1', example);

