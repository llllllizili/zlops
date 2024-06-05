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
          @click="centerDialogVisible = true"
          >文件上传</el-button>



          <el-dialog
                title="提示"
                :visible.sync="centerDialogVisible"
                width="29%"
                center>
            <el-upload
              class="upload-demo"
              drag
              :action="upUrl"
              :file-list="fileList"
              :show-file-list="true"
              :auto-upload="false"
              :on-success="handleAvatarSuccess"
              :headers="upHeaders"
              multiple>
              <i class="el-icon-upload"></i>
              <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
            </el-upload>
            <span slot="footer" class="dialog-footer">
                  <el-button @click="centerDialogVisible = false">取 消</el-button>
                  <el-button type="primary" @click="centerDialogVisible = false">确 定</el-button>
                </span>
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
                <el-link type="primary" :href="scope.row.file" target="_blank">{{ scope.row.name }}</el-link>
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
import { getFileList,upUrl, upHeaders } from "@/api/file"
import Pagination from "@/components/Pagination"
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
  }
};
</script>
