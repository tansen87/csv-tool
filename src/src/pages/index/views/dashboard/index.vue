<template>
  <div>
    <div class="flex">
      <Stat />
    </div>

    <div class="md:flex mt-3">
      <div class="md:flex-1 md:w-0">
        <div class="p-3 bg-normal rounded-sm">
          <div class="flex items-center">
            <div class="flex-1 font-semibold">
              <span v-if="isPath">{{ data.filePath }}</span>
              <span v-else>Convert CSV encoding to another encoding format</span>
            </div>
            <el-button
              type="primary"
              :icon="FolderOpened"
              plain
              @click="openFile()"
            >
              Open File
            </el-button>
          </div>
        </div>

        <div
          class="mt-4 p-3 rounded-sm overflow-hidden bg-normal flex items-center justify-between"
        >
          <div class="flex items-center mr-4">
            <span class="mr-2">Read Encoding:</span>
            <el-select v-model="data.readEncoding" style="width: 120px">
              <el-option label="GBK" value="gbk" />
              <el-option label="UTF-16" value="utf-16" />
              <el-option label="UTF-8" value="utf-8" />
              <el-option label="UTF_8_sig" value="utf_8_sig" />
            </el-select>
          </div>

          <div class="flex items-center ml-4">
            <span class="mr-2">Write Encoding:</span>
            <el-select v-model="data.writeEncoding" style="width: 120px">
              <el-option label="GBK" value="gbk" />
              <el-option label="UTF-16" value="utf-16" />
              <el-option label="UTF-8" value="utf-8" />
              <el-option label="UTF_8_sig" value="utf_8_sig" />
            </el-select>
          </div>

          <el-button
            type="success"
            :loading="isLoading"
            :icon="SwitchFilled"
            plain
            @click="convert()"
            >Convert</el-button
          >
        </div>
      </div>
    </div>

    <div class="md:flex mt-3">
      <el-table
        ref="tableRef"
        :data="tableData"
        :height="formHeight"
        border
        style="width: 100%"
      >
        <el-table-column
          v-for="column in columns"
          :key="column.prop"
          :prop="column.prop"
          :label="column.label"
        />
      </el-table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, reactive, ref } from "vue";
import { ElNotification } from "element-plus";
import { FolderOpened, SwitchFilled } from "@element-plus/icons-vue";

const isPath = ref(false);
const isLoading = ref(false);
const columns = ref([]);
const tableData = ref([]);
const windowHeight = ref(window.innerHeight);
const data = reactive({
  filePath: "",
  readEncoding: "gbk",
  writeEncoding: "utf-8",
});

const formHeight = computed(() => {
  const height = 260;
  return windowHeight.value - height;
});

const updateWindowHeight = () => {
  windowHeight.value = window.innerHeight;
};

onMounted(() => {
  window.addEventListener("resize", updateWindowHeight);
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", updateWindowHeight);
});

// 打开文件
async function openFile() {
  columns.value = [];
  tableData.value = [];
  data.filePath = "";
  isPath.value = false;
  isLoading.value = false;

  window.pywebview.api.system_open_file(data.readEncoding).then((res: any) => {
    if (typeof res === "string" && res.includes("TypeError")) {
      ElNotification({
        title: "TypeError",
        message: "未选择CSV文件",
        position: "bottom-right",
        type: "warning",
      });
      return;
    }

    const parseData = JSON.parse(res);
    const filePath = parseData.file_path;

    if (typeof res === "string" && res.includes("UnicodeError")) {
      ElNotification({
        title: "UnicodeError",
        message: JSON.parse(parseData.json_data),
        position: "bottom-right",
        type: "error",
      });
      data.filePath = filePath;
      return;
    }
    if (typeof res === "string" && res.includes("UnicodeDecodeError")) {
      ElNotification({
        title: "UnicodeDecodeError",
        message: "CSV encoding 有误",
        position: "bottom-right",
        type: "error",
      });
      data.filePath = filePath;
      return;
    }

    const jsonData = JSON.parse(parseData.json_data);

    // 检查 jsonData 是否是数组，如果不是，则将其转换为数组
    const isJsonArray = Array.isArray(jsonData);
    const parseJsonData = isJsonArray ? jsonData : [jsonData];
    columns.value = Object.keys(parseJsonData[0]).map((key) => ({
      name: key,
      label: key,
      prop: key,
    }));
    tableData.value = parseJsonData;
    data.filePath = filePath;
  });

  isPath.value = true;
}

async function convert() {
  if (data.filePath === "") {
    ElNotification({
      title: "TypeError",
      message: "未选择CSV文件",
      position: "bottom-right",
      type: "warning",
    });
    return;
  }

  isLoading.value = true;
  const res = await window.pywebview.api.convert_encoding(
    data.readEncoding,
    data.writeEncoding
  );
  if (typeof res === "string" && res.includes("Error")) {
    ElNotification({
      title: "Encoding Convert Error",
      message: res,
      position: "bottom-right",
      type: "error",
    });
    isLoading.value = false;
  } else if (res && typeof res === "number") {
    ElNotification({
      title: "Convert Done",
      message: "elapsed time: " + res.toString(),
      position: "bottom-right",
      type: "success",
    });
    isLoading.value = false;
  } else {
    ElNotification({
      title: "Encoding Convert Error",
      message: res.toString(),
      position: "bottom-right",
      type: "error",
    });
    isLoading.value = false;
  }
}
</script>
