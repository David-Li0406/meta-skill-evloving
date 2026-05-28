import PptxGenJSType from "pptxgenjs";

//#region src/types.d.ts

type PptxGenJS = PptxGenJSType;
type Slide = PptxGenJSType.Slide;
type TextOptions = PptxGenJSType.TextPropsOptions;
interface ImageOptions {
  path: string;
  x: number;
  y: number;
  w: number;
  h: number;
}
interface TextRun {
  text: string;
  options?: Partial<TextOptions>;
}
interface Shadow {
  type: 'outer' | 'inner' | 'none';
  angle: number;
  blur: number;
  color: string;
  offset: number;
  opacity: number;
}
interface Placeholder {
  id: string;
  x: number;
  y: number;
  w: number;
  h: number;
}
interface Html2PptxOptions {
  tmpDir?: string;
  slide?: Slide | null;
}
interface Html2PptxResult {
  slide: Slide;
  placeholders: Placeholder[];
  html: string;
}
//#endregion
//#region src/index.d.ts

declare function html2pptx(htmlFile: string, pres: PptxGenJS, options?: Html2PptxOptions): Promise<Html2PptxResult>;
//#endregion
export { type Html2PptxOptions, type Html2PptxResult, type ImageOptions, type Placeholder, type PptxGenJS, type Shadow, type Slide, type TextOptions, type TextRun, html2pptx };