#############################################################################
# This is a PoC program to try PyQt Model-View-Delegate approach                #
# It uses table.ui as user interface (a MainWindow with a QTableView on it) #
# A QSqlQuery as a model, and a specific class to deal with delegates       #
#############################################################################
from table_ui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtSql, Qt
from PyQt5 import QtWidgets
import table_ui

class MainWindow(QtWidgets.QMainWindow, table_ui.Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.model = TaskModel(self)
        self.tableView.setModel(self.model)
        self.tableView.setItemDelegate(TaskDelegate())
        # self.model.setTable("tasks")
        # self.model.setEditStrategy(QtSql.QSqlTableModel.EditStrategy.OnManualSubmit)
        # self.model.select()
        #self.model.setHeaderData(0, QtCore.Qt.Horizontal,"ID")

class TaskDelegate(QtWidgets.QStyledItemDelegate):
    COLUMN_TYPES = {1: "combobox", 4: "combobox"}
    COMBO_QUERIES = {1: "SELECT id, title FROM projects ORDER BY title", 4: "SELECT id, name FROM users ORDER BY name"}

    def paint(self, painter: QtGui.QPainter, option: QtWidgets.QStyleOptionViewItem, index: QtCore.QModelIndex):
        l_model = index.model()
        l_value = l_model.record(index.row()).value("status")
        if l_value != "Archive":
            option.font.setBold(True)
        QtWidgets.QStyledItemDelegate.paint(self, painter, option, index)
    
    def createEditor(self, parent: QtWidgets.QWidget, option: QtWidgets.QStyleOptionViewItem, index: QtCore.QModelIndex) -> QtWidgets.QWidget:
        if index.column() not in __class__.COLUMN_TYPES:
            return super().createEditor(parent, option, index)
        l_editor = QtWidgets.QComboBox(parent)
        l_model = QtSql.QSqlQueryModel()
        l_model.setQuery(__class__.COMBO_QUERIES[index.column()])
        l_editor.setModel(l_model)
        l_editor.setModelColumn(1)
        return l_editor

    def setModelData(self, editor: QtWidgets.QWidget, model: QtCore.QAbstractItemModel, index: QtCore.QModelIndex):
        if isinstance(editor, QtWidgets.QComboBox):
            l_combo_model = editor.model()
            l_combo_index = l_combo_model.index(editor.currentIndex(),0)
            l_value = l_combo_model.data(l_combo_index)
            model.setData(index, l_value, QtCore.Qt.EditRole)
        else:
            super().setModelData(editor, model, index)
    

class TaskModel(QtSql.QSqlQueryModel):
    EDITABLE_COLUMNS = {1: "project_id", 2: "status", 3: "`when`", 4: "delegate_id", 5: "estimate", 6: "priority", 7: "title"}

    def __init__(self, parent):
        super().__init__(parent=parent)
        self._sql = """
        SELECT t.id, p.title as project, t.status, t.`when`, u.name as delegate, t.estimate, t.priority, t.title
        FROM tasks t LEFT JOIN projects p ON t.project_id=p.id
        LEFT JOIN users u ON t.delegate_id=u.id
        """
        self.refresh()

    def refresh(self):
        self.setQuery(self._sql)

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlags:
        if index.column() in TaskModel.EDITABLE_COLUMNS:
            return QtSql.QSqlQueryModel.flags(self, index) | QtCore.Qt.ItemIsEditable
        else:
            return QtSql.QSqlQueryModel.flags(self, index)
    

    def setData(self, index: Qt.QModelIndex, value, role: int) -> bool:
        l_col = index.column()
        if l_col not in TaskModel.EDITABLE_COLUMNS.keys():
            return False
        l_pk = self.index(index.row(), 0)
        l_id = self.data(l_pk)
        l_success =  self.updateFieldData(TaskModel.EDITABLE_COLUMNS[l_col], l_id, value)
        self.refresh()

        return l_success
    
    def updateFieldData(self, column, id, value):
        sql = f"UPDATE tasks SET {column}=? WHERE id=?"
        query = QtSql.QSqlQuery()
        query.prepare(sql)
        query.addBindValue(value)
        query.addBindValue(id)
        return query.exec()
        
        

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    db = QtSql.QSqlDatabase().addDatabase('QSQLITE')
    db.setDatabaseName('pyqt.sqlite')
    db.open()
    window = MainWindow()
    window.show()
    app.exec_()