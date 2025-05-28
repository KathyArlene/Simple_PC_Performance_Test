#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多语言支持模块
提供多语言翻译功能
"""

# 支持的语言
SUPPORTED_LANGUAGES = ['zh', 'en', 'ja', 'es']
LANGUAGE_NAMES = {
    'zh': '中文',
    'en': 'English',
    'ja': '日本語',
    'es': 'Español'
}

# 默认语言
DEFAULT_LANGUAGE = 'zh'

# 翻译字典
TRANSLATIONS = {
    # GUI 界面文本
    'window_title': {
        'zh': '电脑性能测试工具',
        'en': 'PC Performance Test Tool',
        'ja': 'パソコン性能テストツール',
        'es': 'Herramienta de Prueba de Rendimiento de PC'
    },
    'test_options': {
        'zh': '测试选项',
        'en': 'Test Options',
        'ja': 'テストオプション',
        'es': 'Opciones de Prueba'
    },
    'cpu_single': {
        'zh': 'CPU单线程',
        'en': 'CPU Single Thread',
        'ja': 'CPUシングルスレッド',
        'es': 'CPU Un Solo Hilo'
    },
    'cpu_multi': {
        'zh': 'CPU多线程',
        'en': 'CPU Multi Thread',
        'ja': 'CPUマルチスレッド',
        'es': 'CPU Multi Hilo'
    },
    'memory': {
        'zh': '内存',
        'en': 'Memory',
        'ja': 'メモリ',
        'es': 'Memoria'
    },
    'disk': {
        'zh': '磁盘I/O',
        'en': 'Disk I/O',
        'ja': 'ディスクI/O',
        'es': 'Disco I/O'
    },
    'gpu': {
        'zh': 'GPU',
        'en': 'GPU',
        'ja': 'GPU',
        'es': 'GPU'
    },
    'start_test': {
        'zh': '开始测试',
        'en': 'Start Test',
        'ja': 'テスト開始',
        'es': 'Iniciar Prueba'
    },
    'save_report': {
        'zh': '保存报告',
        'en': 'Save Report',
        'ja': 'レポート保存',
        'es': 'Guardar Informe'
    },
    'welcome_message': {
        'zh': '欢迎使用电脑性能测试工具！\n\n请选择要运行的测试项目，然后点击\'开始测试\'按钮。\n测试完成后，可以点击\'保存报告\'按钮将结果保存到文件。',
        'en': 'Welcome to PC Performance Test Tool!\n\nPlease select the test items you want to run, then click the \'Start Test\' button.\nAfter the test is completed, you can click the \'Save Report\' button to save the results to a file.',
        'ja': 'パソコン性能テストツールへようこそ！\n\n実行したいテスト項目を選択し、「テスト開始」ボタンをクリックしてください。\nテスト完了後、「レポート保存」ボタンをクリックして結果をファイルに保存できます。',
        'es': '¡Bienvenido a la Herramienta de Prueba de Rendimiento de PC!\n\nSeleccione los elementos de prueba que desea ejecutar, luego haga clic en el botón \'Iniciar Prueba\'.\nDespués de completar la prueba, puede hacer clic en el botón \'Guardar Informe\' para guardar los resultados en un archivo.'
    },
    'warning': {
        'zh': '警告',
        'en': 'Warning',
        'ja': '警告',
        'es': 'Advertencia'
    },
    'select_one_test': {
        'zh': '请至少选择一项测试！',
        'en': 'Please select at least one test!',
        'ja': '少なくとも1つのテストを選択してください！',
        'es': '¡Por favor seleccione al menos una prueba!'
    },
    'completed': {
        'zh': '完成',
        'en': 'Completed',
        'ja': '完了',
        'es': 'Completado'
    },
    'test_completed': {
        'zh': '性能测试已完成！',
        'en': 'Performance test completed!',
        'ja': '性能テストが完了しました！',
        'es': '¡Prueba de rendimiento completada!'
    },
    'error': {
        'zh': '错误',
        'en': 'Error',
        'ja': 'エラー',
        'es': 'Error'
    },
    'test_error': {
        'zh': '测试过程中出现错误:',
        'en': 'Error during test:',
        'ja': 'テスト中にエラーが発生しました:',
        'es': 'Error durante la prueba:'
    },
    'getting_system_info': {
        'zh': '获取系统信息...',
        'en': 'Getting system information...',
        'ja': 'システム情報を取得しています...',
        'es': 'Obteniendo información del sistema...'
    },
    'running_cpu_single_test': {
        'zh': '正在进行CPU单线程测试...',
        'en': 'Running CPU single thread test...',
        'ja': 'CPUシングルスレッドテストを実行しています...',
        'es': 'Ejecutando prueba de CPU de un solo hilo...'
    },
    'running_cpu_multi_test': {
        'zh': '正在进行CPU多线程测试...',
        'en': 'Running CPU multi thread test...',
        'ja': 'CPUマルチスレッドテストを実行しています...',
        'es': 'Ejecutando prueba de CPU multi hilo...'
    },
    'running_memory_test': {
        'zh': '正在进行内存性能测试...',
        'en': 'Running memory performance test...',
        'ja': 'メモリ性能テストを実行しています...',
        'es': 'Ejecutando prueba de rendimiento de memoria...'
    },
    'running_disk_test': {
        'zh': '正在进行磁盘I/O性能测试...',
        'en': 'Running disk I/O performance test...',
        'ja': 'ディスクI/O性能テストを実行しています...',
        'es': 'Ejecutando prueba de rendimiento de disco I/O...'
    },
    'running_gpu_test': {
        'zh': '正在进行GPU性能测试...',
        'en': 'Running GPU performance test...',
        'ja': 'GPU性能テストを実行しています...',
        'es': 'Ejecutando prueba de rendimiento de GPU...'
    },
    'generating_report': {
        'zh': '生成性能测试报告...',
        'en': 'Generating performance test report...',
        'ja': '性能テストレポートを生成しています...',
        'es': 'Generando informe de prueba de rendimiento...'
    },
    'no_results': {
        'zh': '没有可保存的测试结果！',
        'en': 'No test results to save!',
        'ja': '保存するテスト結果がありません！',
        'es': '¡No hay resultados de prueba para guardar!'
    },
    'save_test_report': {
        'zh': '保存测试报告',
        'en': 'Save Test Report',
        'ja': 'テストレポートを保存',
        'es': 'Guardar Informe de Prueba'
    },
    'json_files': {
        'zh': 'JSON文件 (*.json);;所有文件 (*.*)',
        'en': 'JSON Files (*.json);;All Files (*.*)',
        'ja': 'JSONファイル (*.json);;すべてのファイル (*.*)',
        'es': 'Archivos JSON (*.json);;Todos los Archivos (*.*)'
    },
    'success': {
        'zh': '成功',
        'en': 'Success',
        'ja': '成功',
        'es': 'Éxito'
    },
    'report_saved': {
        'zh': '测试报告已保存到:',
        'en': 'Test report has been saved to:',
        'ja': 'テストレポートが保存されました:',
        'es': 'El informe de prueba se ha guardado en:'
    },
    'save_error': {
        'zh': '保存报告时出错:',
        'en': 'Error saving report:',
        'ja': 'レポート保存中にエラーが発生しました:',
        'es': 'Error al guardar el informe:'
    },
    'language': {
        'zh': '语言',
        'en': 'Language',
        'ja': '言語',
        'es': 'Idioma'
    },
    
    # 系统信息
    'system_info': {
        'zh': '系统信息',
        'en': 'System Information',
        'ja': 'システム情報',
        'es': 'Información del Sistema'
    },
    'os': {
        'zh': '操作系统',
        'en': 'Operating System',
        'ja': 'オペレーティングシステム',
        'es': 'Sistema Operativo'
    },
    'processor': {
        'zh': '处理器',
        'en': 'Processor',
        'ja': 'プロセッサ',
        'es': 'Procesador'
    },
    'architecture': {
        'zh': '架构',
        'en': 'Architecture',
        'ja': 'アーキテクチャ',
        'es': 'Arquitectura'
    },
    'physical_cores': {
        'zh': '物理CPU核心',
        'en': 'Physical CPU Cores',
        'ja': '物理CPUコア',
        'es': 'Núcleos Físicos de CPU'
    },
    'logical_cores': {
        'zh': '逻辑CPU核心',
        'en': 'Logical CPU Cores',
        'ja': '論理CPUコア',
        'es': 'Núcleos Lógicos de CPU'
    },
    'physical_cpu_cores': {
        'zh': '物理CPU核心',
        'en': 'Physical CPU Cores',
        'ja': '物理CPUコア',
        'es': 'Núcleos Físicos de CPU'
    },
    'logical_cpu_cores': {
        'zh': '逻辑CPU核心',
        'en': 'Logical CPU Cores',
        'ja': '論理CPUコア',
        'es': 'Núcleos Lógicos de CPU'
    },
    'operating_system': {
        'zh': '操作系统',
        'en': 'Operating System',
        'ja': 'オペレーティングシステム',
        'es': 'Sistema Operativo'
    },
    'total_memory': {
        'zh': '总内存',
        'en': 'Total Memory',
        'ja': '総メモリ',
        'es': 'Memoria Total'
    },
    'available_memory': {
        'zh': '可用内存',
        'en': 'Available Memory',
        'ja': '利用可能なメモリ',
        'es': 'Memoria Disponible'
    },
    'gpu_info': {
        'zh': 'GPU信息',
        'en': 'GPU Information',
        'ja': 'GPU情報',
        'es': 'Información de GPU'
    },
    'video_memory': {
        'zh': '显存',
        'en': 'Video Memory',
        'ja': 'ビデオメモリ',
        'es': 'Memoria de Video'
    },
    'unknown': {
        'zh': '未知',
        'en': 'Unknown',
        'ja': '不明',
        'es': 'Desconocido'
    },
    'gpu_type': {
        'zh': '类型',
        'en': 'Type',
        'ja': 'タイプ',
        'es': 'Tipo'
    },
    'integrated_gpu': {
        'zh': '集成显卡',
        'en': 'Integrated GPU',
        'ja': '内蔵GPU',
        'es': 'GPU Integrada'
    },
    'discrete_gpu': {
        'zh': '独立显卡',
        'en': 'Discrete GPU',
        'ja': '専用GPU',
        'es': 'GPU Discreta'
    },
    'driver_version': {
        'zh': '驱动版本',
        'en': 'Driver Version',
        'ja': 'ドライババージョン',
        'es': 'Versión del Controlador'
    },
    
    # 测试报告
    'performance_test': {
        'zh': '性能测试',
        'en': 'Performance Test',
        'ja': '性能テスト',
        'es': 'Prueba de Rendimiento'
    },
    'start_performance_test': {
        'zh': '开始性能测试...',
        'en': 'Starting performance test...',
        'ja': '性能テストを開始しています...',
        'es': 'Iniciando prueba de rendimiento...'
    },
    'cpu_test': {
        'zh': 'CPU性能测试',
        'en': 'CPU Performance Test',
        'ja': 'CPU性能テスト',
        'es': 'Prueba de Rendimiento de CPU'
    },
    'memory_test': {
        'zh': '内存性能测试',
        'en': 'Memory Performance Test',
        'ja': 'メモリ性能テスト',
        'es': 'Prueba de Rendimiento de Memoria'
    },
    'disk_test': {
        'zh': '磁盘I/O性能测试',
        'en': 'Disk I/O Performance Test',
        'ja': 'ディスクI/O性能テスト',
        'es': 'Prueba de Rendimiento de Disco I/O'
    },
    'gpu_test': {
        'zh': 'GPU性能测试',
        'en': 'GPU Performance Test',
        'ja': 'GPU性能テスト',
        'es': 'Prueba de Rendimiento de GPU'
    },
    'performance_report': {
        'zh': '性能测试报告',
        'en': 'Performance Test Report',
        'ja': '性能テストレポート',
        'es': 'Informe de Prueba de Rendimiento'
    },
    'cpu_single_score': {
        'zh': 'CPU单线程性能得分',
        'en': 'CPU Single Thread Performance Score',
        'ja': 'CPUシングルスレッド性能スコア',
        'es': 'Puntuación de Rendimiento de CPU de Un Solo Hilo'
    },
    'cpu_multi_score': {
        'zh': 'CPU多线程性能得分',
        'en': 'CPU Multi Thread Performance Score',
        'ja': 'CPUマルチスレッド性能スコア',
        'es': 'Puntuación de Rendimiento de CPU Multi Hilo'
    },
    'memory_score': {
        'zh': '内存性能得分',
        'en': 'Memory Performance Score',
        'ja': 'メモリ性能スコア',
        'es': 'Puntuación de Rendimiento de Memoria'
    },
    'disk_write_score': {
        'zh': '磁盘写入性能得分',
        'en': 'Disk Write Performance Score',
        'ja': 'ディスク書き込み性能スコア',
        'es': 'Puntuación de Rendimiento de Escritura de Disco'
    },
    'disk_read_score': {
        'zh': '磁盘读取性能得分',
        'en': 'Disk Read Performance Score',
        'ja': 'ディスク読み取り性能スコア',
        'es': 'Puntuación de Rendimiento de Lectura de Disco'
    },
    'gpu_score': {
        'zh': 'GPU性能得分',
        'en': 'GPU Performance Score',
        'ja': 'GPU性能スコア',
        'es': 'Puntuación de Rendimiento de GPU'
    },
    'total_score': {
        'zh': '综合性能得分',
        'en': 'Total Performance Score',
        'ja': '総合性能スコア',
        'es': 'Puntuación de Rendimiento Total'
    },
    'detailed_report_saved': {
        'zh': '详细报告已保存到',
        'en': 'Detailed report has been saved to',
        'ja': '詳細なレポートが保存されました',
        'es': 'El informe detallado se ha guardado en'
    },
    'test_interrupted': {
        'zh': '测试被用户中断',
        'en': 'Test interrupted by user',
        'ja': 'テストがユーザーによって中断されました',
        'es': 'Prueba interrumpida por el usuario'
    },
    'test_error_occurred': {
        'zh': '测试过程中出现错误',
        'en': 'Error occurred during test',
        'ja': 'テスト中にエラーが発生しました',
        'es': 'Se produjo un error durante la prueba'
    },
    'error_getting_gpu_info': {
        'zh': '获取GPU信息时出错',
        'en': 'Error getting GPU information',
        'ja': 'GPU情報の取得中にエラーが発生しました',
        'es': 'Error al obtener información de GPU'
    },
    'wmi_not_installed': {
        'zh': 'WMI库未安装',
        'en': 'WMI library not installed',
        'ja': 'WMIライブラリがインストールされていません',
        'es': 'Biblioteca WMI no instalada'
    },
    'warning_wmi_not_installed': {
        'zh': '警告: 未安装wmi库，GPU信息检测将不可用。请使用 \'pip install wmi\' 安装。',
        'en': 'Warning: wmi library not installed, GPU information detection will not be available. Please install using \'pip install wmi\'.',
        'ja': '警告: wmiライブラリがインストールされていないため、GPU情報の検出は利用できません。\'pip install wmi\'を使用してインストールしてください。',
        'es': 'Advertencia: biblioteca wmi no instalada, la detección de información de GPU no estará disponible. Instale usando \'pip install wmi\'.'  
    },
    
    # CLI 参数
    'cli_description': {
        'zh': '电脑性能测试工具',
        'en': 'PC Performance Test Tool',
        'ja': 'パソコン性能テストツール',
        'es': 'Herramienta de Prueba de Rendimiento de PC'
    },
    'cli_cpu_help': {
        'zh': '仅运行CPU测试',
        'en': 'Run CPU test only',
        'ja': 'CPUテストのみを実行',
        'es': 'Ejecutar solo prueba de CPU'
    },
    'cli_memory_help': {
        'zh': '仅运行内存测试',
        'en': 'Run memory test only',
        'ja': 'メモリテストのみを実行',
        'es': 'Ejecutar solo prueba de memoria'
    },
    'cli_disk_help': {
        'zh': '仅运行磁盘I/O测试',
        'en': 'Run disk I/O test only',
        'ja': 'ディスクI/Oテストのみを実行',
        'es': 'Ejecutar solo prueba de disco I/O'
    },
    'cli_gpu_help': {
        'zh': '仅运行GPU测试',
        'en': 'Run GPU test only',
        'ja': 'GPUテストのみを実行',
        'es': 'Ejecutar solo prueba de GPU'
    },
    'cli_all_help': {
        'zh': '运行所有测试（默认）',
        'en': 'Run all tests (default)',
        'ja': 'すべてのテストを実行（デフォルト）',
        'es': 'Ejecutar todas las pruebas (predeterminado)'
    },
    'cli_output_help': {
        'zh': '指定报告输出文件路径',
        'en': 'Specify report output file path',
        'ja': 'レポート出力ファイルパスを指定',
        'es': 'Especificar ruta de archivo de salida del informe'
    },
    'cli_quiet_help': {
        'zh': '安静模式，仅显示最终结果',
        'en': 'Quiet mode, show only final results',
        'ja': '静かモード、最終結果のみを表示',
        'es': 'Modo silencioso, mostrar solo resultados finales'
    },
    'cli_language_help': {
        'zh': '设置语言 (zh: 中文, en: 英文, ja: 日文, es: 西班牙语)',
        'en': 'Set language (zh: Chinese, en: English, ja: Japanese, es: Spanish)',
        'ja': '言語を設定 (zh: 中国語, en: 英語, ja: 日本語, es: スペイン語)',
        'es': 'Establecer idioma (zh: Chino, en: Inglés, ja: Japonés, es: Español)'
    },
    'cli_welcome': {
        'zh': '电脑性能测试工具 - 命令行版本',
        'en': 'PC Performance Test Tool - Command Line Version',
        'ja': 'パソコン性能テストツール - コマンドライン版',
        'es': 'Herramienta de Prueba de Rendimiento de PC - Versión de Línea de Comandos'
    },
    'cli_start_selected': {
        'zh': '开始选定的性能测试...',
        'en': 'Starting selected performance tests...',
        'ja': '選択された性能テストを開始しています...',
        'es': 'Iniciando pruebas de rendimiento seleccionadas...'
    },
    
    # 打包脚本
    'build_title': {
        'zh': '电脑性能测试工具 - 打包脚本',
        'en': 'PC Performance Test Tool - Build Script',
        'ja': 'パソコン性能テストツール - ビルドスクリプト',
        'es': 'Herramienta de Prueba de Rendimiento de PC - Script de Compilación'
    },
    'missing_dependencies': {
        'zh': '缺少必要的依赖包',
        'en': 'Missing required dependencies',
        'ja': '必要な依存関係が不足しています',
        'es': 'Faltan dependencias requeridas'
    },
    'auto_install': {
        'zh': '是否自动安装这些依赖? (y/n)',
        'en': 'Do you want to automatically install these dependencies? (y/n)',
        'ja': 'これらの依存関係を自動的にインストールしますか？ (y/n)',
        'es': '¿Desea instalar automáticamente estas dependencias? (y/n)'
    },
    'installing': {
        'zh': '正在安装',
        'en': 'Installing',
        'ja': 'インストール中',
        'es': 'Instalando'
    },
    'manual_install': {
        'zh': '请手动安装缺少的依赖后再运行此脚本。',
        'en': 'Please manually install the missing dependencies before running this script.',
        'ja': 'このスクリプトを実行する前に、不足している依存関係を手動でインストールしてください。',
        'es': 'Por favor, instale manualmente las dependencias faltantes antes de ejecutar este script.'
    },
    'start_packaging': {
        'zh': '开始打包程序...',
        'en': 'Starting to package the program...',
        'ja': 'プログラムのパッケージ化を開始しています...',
        'es': 'Comenzando a empaquetar el programa...'
    },
    'packaging_completed': {
        'zh': '打包完成!',
        'en': 'Packaging completed!',
        'ja': 'パッケージ化が完了しました！',
        'es': '¡Empaquetado completado!'
    },
    'executable_location': {
        'zh': '可执行文件位置',
        'en': 'Executable file location',
        'ja': '実行可能ファイルの場所',
        'es': 'Ubicación del archivo ejecutable'
    },
    'packaging_error': {
        'zh': '打包过程中出错',
        'en': 'Error during packaging',
        'ja': 'パッケージ化中にエラーが発生しました',
        'es': 'Error durante el empaquetado'
    },
    'missing_source_files': {
        'zh': '错误: 缺少必要的源文件',
        'en': 'Error: Missing required source files',
        'ja': 'エラー：必要なソースファイルが不足しています',
        'es': 'Error: Faltan archivos fuente requeridos'
    },
    'ensure_all_files': {
        'zh': '请确保所有源文件都在当前目录中。',
        'en': 'Please ensure all source files are in the current directory.',
        'ja': 'すべてのソースファイルが現在のディレクトリにあることを確認してください。',
        'es': 'Por favor, asegúrese de que todos los archivos fuente estén en el directorio actual.'
    },
    'icon_tip': {
        'zh': '提示: 如果您想要添加图标，请修改打包命令添加 --icon=your_icon.ico 参数。',
        'en': 'Tip: If you want to add an icon, please modify the packaging command to add the --icon=your_icon.ico parameter.',
        'ja': 'ヒント：アイコンを追加したい場合は、パッケージングコマンドを変更して --icon=your_icon.ico パラメータを追加してください。',
        'es': 'Consejo: Si desea agregar un icono, modifique el comando de empaquetado para agregar el parámetro --icon=your_icon.ico.'
    }
}


class Language:
    """语言类，用于处理多语言支持"""
    def __init__(self, lang_code=DEFAULT_LANGUAGE):
        """初始化语言类
        
        Args:
            lang_code: 语言代码，默认为中文
        """
        self.set_language(lang_code)
    
    def set_language(self, lang_code):
        """设置语言
        
        Args:
            lang_code: 语言代码
        """
        if lang_code not in SUPPORTED_LANGUAGES:
            lang_code = DEFAULT_LANGUAGE
        self.lang_code = lang_code
    
    def get(self, key):
        """获取翻译文本
        
        Args:
            key: 翻译键值
            
        Returns:
            str: 翻译后的文本
        """
        if key not in TRANSLATIONS:
            return key
        
        if self.lang_code not in TRANSLATIONS[key]:
            return TRANSLATIONS[key][DEFAULT_LANGUAGE]
        
        return TRANSLATIONS[key][self.lang_code]


# 全局语言实例
_lang = Language()


def set_language(lang_code):
    """设置全局语言
    
    Args:
        lang_code: 语言代码
    """
    global _lang
    _lang.set_language(lang_code)


def get(key):
    """获取翻译文本
    
    Args:
        key: 翻译键值
        
    Returns:
        str: 翻译后的文本
    """
    global _lang
    return _lang.get(key)


def get_language_code():
    """获取当前语言代码
    
    Returns:
        str: 当前语言代码
    """
    global _lang
    return _lang.lang_code


if __name__ == "__main__":
    # 测试代码
    print("语言模块测试")
    print("=" * 60)
    
    # 测试中文
    set_language('zh')
    print(f"当前语言: {get_language_code()} ({LANGUAGE_NAMES[get_language_code()]})")
    print(f"窗口标题: {get('window_title')}")
    print(f"开始测试按钮: {get('start_test')}")
    print()
    
    # 测试英文
    set_language('en')
    print(f"Current Language: {get_language_code()} ({LANGUAGE_NAMES[get_language_code()]})")
    print(f"Window Title: {get('window_title')}")
    print(f"Start Test Button: {get('start_test')}")
    print()
    
    # 测试日文
    set_language('ja')
    print(f"現在の言語: {get_language_code()} ({LANGUAGE_NAMES[get_language_code()]})")
    print(f"ウィンドウタイトル: {get('window_title')}")
    print(f"テスト開始ボタン: {get('start_test')}")
    print()
    
    # 测试西班牙语
    set_language('es')
    print(f"Idioma Actual: {get_language_code()} ({LANGUAGE_NAMES[get_language_code()]})")
    print(f"Título de la Ventana: {get('window_title')}")
    print(f"Botón de Inicio de Prueba: {get('start_test')}")