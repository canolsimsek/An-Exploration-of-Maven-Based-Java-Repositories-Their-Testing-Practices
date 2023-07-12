import os
import chardet
import javalang
import glob
import pandas as pd

class TestClassCounter:
    @staticmethod
    def count_classes(contents):
        try:
            tree = javalang.parse.parse(contents)
        except javalang.parser.JavaSyntaxError as e:
            print(f"Syntax error: {e}")
            return 0, []

        classes = [(path, node) for path, node in tree.filter(javalang.tree.ClassDeclaration)]
        test_classes = [c for c in classes if "Test" in c[1].name]
        test_class_names = [c[1].name for c in test_classes]
        return len(test_classes), test_class_names

class TestMethodCounter:
    @staticmethod
    def count_methods(contents):
        try:
            tree = javalang.parse.parse(contents)
        except javalang.parser.JavaSyntaxError as e:
            print(f"Syntax error: {e}")
            return 0, [], 0

        methods = [(path, node) for path, node in tree.filter(javalang.tree.MethodDeclaration)]
        test_method_names = [m[1].name for m in methods]

        # Approximate total lines of code in the test methods
        tloc = 0
        for i in range(len(methods)-1):
            tloc += methods[i+1][1].position.line - methods[i][1].position.line

        return len(methods), test_method_names, tloc


class RepoParser:
    @staticmethod
    def get_repos(directory="."):
        repos = []
        for root, dirs, _ in os.walk(directory):
            if ".git" in dirs:
                repos.append(root)
                dirs.remove(".git")
        return repos

    @staticmethod
    def get_test_files(repo_path):
        return glob.glob(os.path.join(repo_path, "**", "test", "**", "*.java"), recursive=True)

class FileUtils:
    @staticmethod
    def read_file(file_path, encoding):
        try:
            with open(file_path, "r", encoding=encoding) as f:
                contents = f.read()
            return contents
        except UnicodeDecodeError:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    contents = f.read()
                return contents
            except Exception as e:
                print(f"Failed to read file {file_path} due to: {e}")

    @staticmethod
    def detect_encoding(file_path):
        with open(file_path, "rb") as f:
            result = chardet.detect(f.read())
        return result["encoding"]

class Main:
    @staticmethod
    def main():
        root_folder = r"D:\deneme3\ecommerce\New folder"
        repo_parser = RepoParser()
        repo_list = repo_parser.get_repos(root_folder)

        test_class_counter = TestClassCounter()
        test_method_counter = TestMethodCounter()
        file_utils = FileUtils()

        data = []

        for repo in repo_list:
            print(f"Processing {repo}")
            java_test_files = repo_parser.get_test_files(repo)

            for file_path in java_test_files:
                print(f"Processing {file_path}")

                try:
                    with open(file_path, 'rb') as f:
                        rawdata = f.read()
                    encoding = chardet.detect(rawdata)['encoding']
                    contents = file_utils.read_file(file_path, encoding)
                    test_class_count, test_class_names = test_class_counter.count_classes(contents)
                    test_method_count, test_method_names, tloc = test_method_counter.count_methods(contents)

                    # Only append data to the list if test class count and test method count are both greater than 0
                    if test_class_count > 0 and test_method_count > 0:
                        data.append([repo, file_path, test_class_count, ", ".join(test_class_names), test_method_count, ", ".join(test_method_names), tloc])

                except Exception as e:
                    print(f"Error processing {file_path}, skipped due to: {e}")

        df = pd.DataFrame(data, columns=["Repository", "File Path", "Test Class Count", "Test Classes", "Test Method Count", "Test Methods", "TLOC"])

        # Group by repository and compute the sums of "Test Class Count", "Test Method Count", and "TLOC"
        df_summary = df.groupby("Repository").agg({"Test Class Count": "sum", "Test Method Count": "sum", "TLOC": "sum"}).reset_index()

        # Save the data and summary sheets in the Excel file
        with pd.ExcelWriter(os.path.join(root_folder, "ecomresults.xlsx")) as writer:
            df.to_excel(writer, sheet_name='Data', index=False)
            df_summary.to_excel(writer, sheet_name='Summary', index=False)

if __name__ == "__main__":
    Main.main()
