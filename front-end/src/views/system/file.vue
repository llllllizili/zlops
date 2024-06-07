<template>
  <div class="app-container">
        <div>
          <el-select
            v-model="listQuery.type"
            placeholder="文件类型"
            clearable
            style="width: 200px"
            class="filter-item"
            @change="handleFilter"
          >
            <el-option
              v-for="item in enabledOptions"
              :key="item.key"
              :label="item.display_name"
              :value="item.key"
            />
          </el-select>
          <el-input
            v-model="listQuery.search"
            placeholder="文件名"
            style="width: 300px;"
            class="filter-item"
            @keyup.enter.native="handleFilter"
          />
          <el-button
            class="filter-item"
            type="primary"
            icon="el-icon-search"
            @click="handleFilter"
            size="small"
          >搜索</el-button>
          <el-button
            class="filter-item"
            type="primary"
            icon="el-icon-refresh-left"
            @click="resetFilter"
            size="small"
          >重置</el-button>
          <el-button 
          type="primary" 
          size="small"
          v-if="checkPermission(['file_upload'])"
          @click="centerDialogVisible = true"
          >文件上传</el-button>

          <el-dialog
                title="自动上传"
                :visible.sync="centerDialogVisible"
                width="26%"
                center>
            <el-upload
              class="upload-demo"
              drag
              :action="upUrl"
              :file-list="fileList"
              :show-file-list="true"
              :auto-upload="true"
              :on-success="handleFileUploadSuccess"
              :before-upload="beforeAvatarUpload"
              :on-error="handleFileUploadError"
              :headers="upHeaders"
              multiple>
              <i class="el-icon-upload"></i>
              <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
            </el-upload>
            <!-- <span slot="footer" class="dialog-footer">
                  <el-button @click="centerDialogVisible = false">取 消</el-button>
                  <el-button type="primary" @click="centerDialogVisible = false">确 定</el-button>
            </span> -->
          </el-dialog>
        </div>
        <el-table
          v-loading="listLoading"
          :data="fileList.results"
          style="width: 100%;margin-top:10px;"
          highlight-current-row
          row-key="id"
          height="100"
          stripe
          border
          v-el-height-adaptive-table="{bottomOffset: 50}"
        >
          <el-table-column type="index" width="50" />
          <el-table-column align="center" label="名称">
            <template slot-scope="scope">
                <el-link
                type="primary"
                :disabled="!checkPermission(['file_view'])"
                :href="scope.row.file"
                target="_blank">{{ scope.row.name }}
              </el-link>
            </template>
          </el-table-column>
          <el-table-column align="header-center" label="类型">
            <template slot-scope="scope">{{ scope.row.type }}</template>
          </el-table-column>
          <el-table-column align="header-center" label="格式">
            <template slot-scope="scope">{{ scope.row.mime }}</template>
          </el-table-column>
          <el-table-column align="header-center" label="大小(B)">
            <template slot-scope="scope">{{ scope.row.size }}</template>
          </el-table-column>
          <el-table-column align="header-center" label="地址">
            <template slot-scope="scope">{{ scope.row.path }}</template>
          </el-table-column>
          <el-table-column label="上传日期">
            <template slot-scope="scope">
              <span>{{ scope.row.create_time }}</span>
            </template>
          </el-table-column>
          <el-table-column align="center" label="操作">
        <template slot-scope="scope">
          <el-button
            type="danger"
            size="small"
            icon="el-icon-delete"
            v-if="checkPermission(['file_delete'])"
            @click="handleDelete(scope)"
          />
        </template>
      </el-table-column>
        </el-table>

        <pagination
          v-show="fileList.count>0"
          :total="fileList.count"
          :page.sync="listQuery.page"
          :limit.sync="listQuery.page_size"
          @pagination="getList"
        />
  </div>
</template>
<script>
import { getFileList,upUrl, upHeaders, deleteFile } from "@/api/file"
import Pagination from "@/components/Pagination"
import checkPermission from "@/utils/permission"

export default {
  components: { Pagination },
  data() {
    return {
      centerDialogVisible: false,
      fileList: {count:0},
      upHeaders: upHeaders(),
      upUrl: upUrl(),
      listLoading: true,
      listQuery: {
        page: 1,
        page_size: 20
      },
      enabledOptions: [
        { key: "文档", display_name: "文档" },
        { key: "图片", display_name: "图片" },
        { key: "音频", display_name: "音频" },
        { key: "视频", display_name: "视频" },
        { key: "其它", display_name: "其它" }
      ],
    };
  },
  created() {
    this.getList();
  },
  methods: {
    checkPermission,
    handleFileUploadSuccess() {
      this.getList();
      this.$message.success("上传成功")
    },
    handleFileUploadError() {
      this.$message.error("上传失败")
    },
    beforeAvatarUpload(file) {
      const isLt5M = file.size / 1024 / 1024 < 5;
      if (!isLt5M) {
        this.$message.error("上传文件不能超过5MB!");
      }
      return isLt5M;
    },
    getList() {
      this.listLoading = true;
      getFileList(this.listQuery).then(response => {
        if (response.data) {
          this.fileList = response.data
        }
        this.listLoading = false;
      });
    },
    resetFilter() {
      this.listQuery = {
        page: 1,
        page_size: 20
      };
      this.getList();
    },
    handleFilter() {
      this.listQuery.page = 1;
      this.getList();
    },
    handleDelete(scope) {
      this.$confirm("确认删除?", "警告", {
        confirmButtonText: "确认",
        cancelButtonText: "取消",
        type: "error",
      })
        .then(async () => {
          await deleteFile(scope.row.id);
          this.getList();
          this.$message({
            type: "success",
            message: "成功删除!",
          });
        })
        .catch((err) => {
          console.error(err);
        });
    },
  }
};
</script>
