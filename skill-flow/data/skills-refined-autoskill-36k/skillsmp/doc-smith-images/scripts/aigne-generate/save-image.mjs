import fs from "node:fs/promises";
import path from "node:path";

/**
 * 将 Image Agent 生成的图片保存到指定路径
 */
export default async function saveImage(input) {
  const { images, savePath } = input;

  // 验证输入
  if (!images || !Array.isArray(images) || images.length === 0) {
    return { message: "保存失败：输入中没有图片数据" };
  }

  if (!savePath) {
    return { message: "保存失败：未指定保存路径" };
  }

  const sourceImage = images[0];
  const sourcePath = sourceImage.path;

  // 检查源文件是否存在
  try {
    await fs.access(sourcePath);
  } catch {
    return { message: `保存失败：源图片文件不存在 (${sourcePath})` };
  }

  // 确保输出目录存在
  const outputDir = path.dirname(savePath);
  await fs.mkdir(outputDir, { recursive: true });

  // 复制图片到目标路径
  try {
    await fs.copyFile(sourcePath, savePath);
    const stats = await fs.stat(savePath);
    const sizeKB = (stats.size / 1024).toFixed(1);

    return { message: `图片已保存到 ${savePath}（${sizeKB} KB）` };
  } catch (err) {
    return { message: `保存失败：${err.message}` };
  }
}

saveImage.description = "Save generated image to specified path";
saveImage.input_schema = {
  type: "object",
  properties: {
    images: {
      type: "array",
      description: "Image Agent output - array of generated images",
      items: {
        type: "object",
        properties: {
          path: { type: "string" },
          filename: { type: "string" },
          mimeType: { type: "string" },
        },
      },
    },
    savePath: {
      type: "string",
      description: "Output file path to save the image",
    },
  },
  required: ["images", "savePath"],
};
saveImage.output_schema = {
  type: "object",
  properties: {
    message: { type: "string", description: "执行结果的自然语言描述" },
  },
};
