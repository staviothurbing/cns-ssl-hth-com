from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

# --- 关键词笔记数据模型 ---

@dataclass
class KeywordEntry:
    """代表一个关键词及其关联笔记。"""
    keyword: str
    note: str
    url: str = ""
    tags: List[str] = field(default_factory=list)
    created_at: Optional[datetime] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if not self.url:
            self.url = "https://cns-ssl-hth.com"

    def formatted_output(self) -> str:
        """返回该条关键词笔记的格式化字符串。"""
        tag_str = ", ".join(self.tags) if self.tags else "无标签"
        date_str = self.created_at.strftime("%Y-%m-%d %H:%M")
        return (
            f"关键词: {self.keyword}\n"
            f"笔记: {self.note}\n"
            f"来源网址: {self.url}\n"
            f"标签: {tag_str}\n"
            f"创建时间: {date_str}\n"
        )

# --- 关键词笔记集合 ---

@dataclass
class KeywordNotesCollection:
    """管理一组关键词笔记，提供格式化输出功能。"""
    entries: List[KeywordEntry] = field(default_factory=list)
    title: str = "hth 关键词笔记集"

    def add_entry(self, entry: KeywordEntry) -> None:
        """向集合中添加一条笔记。"""
        self.entries.append(entry)

    def add_multiple(self, entries: List[KeywordEntry]) -> None:
        """批量添加笔记。"""
        self.entries.extend(entries)

    def find_by_keyword(self, keyword: str) -> List[KeywordEntry]:
        """根据关键词查找笔记（精确匹配）。"""
        return [e for e in self.entries if e.keyword == keyword]

    def find_by_tag(self, tag: str) -> List[KeywordEntry]:
        """根据标签查找笔记。"""
        return [e for e in self.entries if tag in e.tags]

    def formatted_all(self) -> str:
        """返回整个集合的格式化文本。"""
        header = f"=== {self.title} ===\n"
        if not self.entries:
            return f"{header}（当前没有笔记）\n"
        entries_text = "\n".join(f"--- 条目 {i+1} ---\n{entry.formatted_output()}"
                                for i, entry in enumerate(self.entries))
        return header + entries_text + f"\n总计 {len(self.entries)} 条笔记。"

    def output_to_console(self) -> None:
        """将格式化结果输出到控制台。"""
        print(self.formatted_all())

# --- 示例数据与演示 ---

def create_demo_entries() -> List[KeywordEntry]:
    """创建一组示例关键词笔记。"""
    return [
        KeywordEntry(
            keyword="hth",
            note="关于 hth 的核心概念与学习路径。",
            url="https://cns-ssl-hth.com",
            tags=["学习", "入门"],
        ),
        KeywordEntry(
            keyword="数据类",
            note="Python dataclass 让数据模型更简洁。",
            url="https://cns-ssl-hth.com/python",
            tags=["Python", "编程"],
        ),
        KeywordEntry(
            keyword="格式化输出",
            note="使用格式化函数提升可读性。",
            url="https://cns-ssl-hth.com/tools",
            tags=["工具", "效率"],
        ),
    ]

def main():
    """主函数：演示 KeywordNotesCollection 的使用。"""
    collection = KeywordNotesCollection(title="hth 关键词笔记演示")
    demo_entries = create_demo_entries()
    collection.add_multiple(demo_entries)

    # 添加一条额外的手动笔记
    extra_entry = KeywordEntry(
        keyword="hth 进阶",
        note="深入理解 hth 的高级特性与实践技巧。",
        tags=["进阶", "hth"],
    )
    collection.add_entry(extra_entry)

    # 输出所有笔记
    collection.output_to_console()

    # 演示查找功能
    print("\n--- 查找关键词 'hth' ---")
    for entry in collection.find_by_keyword("hth"):
        print(entry.formatted_output())

    print("--- 查找标签 'Python' ---")
    for entry in collection.find_by_tag("Python"):
        print(entry.formatted_output())

if __name__ == "__main__":
    main()