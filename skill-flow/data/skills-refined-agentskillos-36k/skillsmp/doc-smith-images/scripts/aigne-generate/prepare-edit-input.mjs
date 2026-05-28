import { basename } from "node:path";
import { access, constants } from "node:fs/promises";

/**
 * 准备图片编辑的输入参数
 * 将编辑请求转换为 generate-image.yaml 所需的 image-to-image 格式
 *
 * @param {Object} input - 输入参数
 * @param {string} input.desc - 编辑要求/修改说明
 * @param {string} input.sourcePath - 源图片路径
 * @param {string} input.savePath - 输出文件路径
 * @param {string} input.sourceLocale - 源图片语言
 * @param {string} input.targetLocale - 目标语言（翻译场景）
 * @param {string} input.aspectRatio - 宽高比
 * @param {string} input.size - 图片尺寸
 * @returns {Promise<Object>} - 准备好的输入参数
 */
export default async function prepareEditInput(input) {
  const {
    desc,
    sourcePath,
    savePath,
    sourceLocale = "zh",
    targetLocale = "",
    aspectRatio = "4:3",
    size = "2K",
  } = input;

  try {
    // 验证源图片存在
    await access(sourcePath, constants.R_OK);

    // 确定 MIME 类型
    const ext = sourcePath.toLowerCase();
    let mimeType = "image/png";
    if (ext.endsWith(".jpg") || ext.endsWith(".jpeg")) {
      mimeType = "image/jpeg";
    } else if (ext.endsWith(".webp")) {
      mimeType = "image/webp";
    }

    // 构建 existingImage 参数（mediaFile 格式）
    const existingImage = [
      {
        type: "local",
        path: sourcePath,
        filename: basename(sourcePath),
        mimeType,
      },
    ];

    // 构建编辑描述
    let editDesc = desc;

    // 如果是翻译场景，增强描述
    if (targetLocale && targetLocale !== sourceLocale) {
      editDesc = `将图片中的文字从 ${sourceLocale} 翻译成 ${targetLocale}。${desc}`;
    }

    // 确定目标语言（用于图片中的文字）
    const locale = targetLocale || sourceLocale;

    return {
      success: true,
      // 传递给 generate-image.yaml 的参数
      desc: editDesc,
      documentContent: "", // 编辑模式不需要文档内容
      locale,
      size,
      aspectRatio,
      existingImage,
      useImageToImage: true,
      feedback: desc, // 将编辑要求作为 feedback 传递
      // 传递给 save-image.mjs 的参数
      savePath,
      message: `准备编辑图片: ${sourcePath} → ${savePath}`,
    };
  } catch (error) {
    if (error.code === "ENOENT") {
      return {
        success: false,
        error: "SOURCE_NOT_FOUND",
        message: `源图片不存在: ${sourcePath}`,
        suggestion: "请检查图片路径是否正确",
      };
    }
    return {
      success: false,
      error: "UNEXPECTED_ERROR",
      message: `准备图片编辑输入时发生错误: ${error.message}`,
    };
  }
}

// 添加描述信息
prepareEditInput.description =
  "准备图片编辑的输入参数，将编辑请求转换为 generate-image.yaml 所需的 image-to-image 格式。" +
  "支持图片翻译、样式调整、内容修改等场景。";

// 定义输入 schema
prepareEditInput.input_schema = {
  type: "object",
  required: ["desc", "sourcePath", "savePath"],
  properties: {
    desc: {
      type: "string",
      description: "编辑要求/修改说明",
    },
    sourcePath: {
      type: "string",
      description: "源图片路径（要编辑的图片）",
    },
    savePath: {
      type: "string",
      description: "输出文件路径",
    },
    sourceLocale: {
      type: "string",
      description: "源图片的语言",
      default: "zh",
    },
    targetLocale: {
      type: "string",
      description: "目标语言（用于翻译场景）",
      default: "",
    },
    aspectRatio: {
      type: "string",
      description: "宽高比",
      default: "4:3",
    },
    size: {
      type: "string",
      description: "图片尺寸",
      default: "2K",
    },
  },
};

// 定义输出 schema
prepareEditInput.output_schema = {
  type: "object",
  required: ["success"],
  properties: {
    success: {
      type: "boolean",
      description: "操作是否成功",
    },
    desc: {
      type: "string",
      description: "编辑描述（可能经过增强）",
    },
    documentContent: {
      type: "string",
      description: "文档内容（编辑模式为空）",
    },
    locale: {
      type: "string",
      description: "目标语言",
    },
    size: {
      type: "string",
      description: "图片尺寸",
    },
    aspectRatio: {
      type: "string",
      description: "宽高比",
    },
    existingImage: {
      type: "array",
      description: "源图片 mediaFile 对象数组",
      items: { type: "object" },
    },
    useImageToImage: {
      type: "boolean",
      description: "是否使用 image-to-image 模式",
    },
    feedback: {
      type: "string",
      description: "用户反馈/编辑要求",
    },
    savePath: {
      type: "string",
      description: "输出文件路径",
    },
    message: {
      type: "string",
      description: "操作结果描述",
    },
    error: {
      type: "string",
      description: "错误代码（失败时存在）",
    },
    suggestion: {
      type: "string",
      description: "建议操作（失败时存在）",
    },
  },
};
