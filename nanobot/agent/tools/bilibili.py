"""B站工具：获取B站用户信息和动态。"""

import json
import os
from typing import Any

from nanobot.agent.tools.base import Tool


class BilibiliTool(Tool):
    """获取B站用户信息和动态。"""
    
    name = "bilibili"
    description = "获取B站用户信息和动态，返回用户基本信息和最新动态。支持获取所有动态。"
    def __init__(self):
        """初始化B站工具，读取默认cookie。"""
        super().__init__()
    
    parameters = {
        "type": "object",
        "properties": {
            "uid": {"type": "string", "description": "B站用户UID"},
            "cookie": {"type": "string", "description": "B站登录Cookie（可选，用于需要登录的操作"},
            "action": {"type": "string", "enum": ["info", "dynamic", "all_dynamics"], "default": "info", "description": "操作类型：info（用户信息）、dynamic（用户最新动态）、all_dynamics（所有动态）"},
            "limit": {"type": "integer", "description": "获取动态的数量限制（仅用于all_dynamics）", "minimum": 1, "maximum": 100, "default": 20}
        },
        "required": ["uid"]
    }
    
    async def execute(self, uid: str, cookie: str | None = None, action: str = "info", limit: int = 20, **kwargs: Any) -> str:
        """执行B站API操作（使用 bilibili-api-python 库）。"""
        try:
            from bilibili_api import user, Credential
            
            uid_int = int(uid)
            u = user.User(uid_int)
            
            if action == "info":
                # 获取用户信息
                info = await u.get_user_info()
                
                result = {
                    "type": "user_info",
                    "data": {
                        "uid": info.get("mid", ""),
                        "name": info.get("name", ""),
                        "sign": info.get("sign", ""),
                        "avatar": info.get("face", ""),
                        "level": info.get("level", 0),
                        "sex": info.get("sex", ""),
                        "birthday": info.get("birthday", ""),
                        "fans_badge": info.get("fans_badge", False),
                        "raw": info
                    }
                }
                
                return json.dumps(result, ensure_ascii=False)
                
            elif action == "dynamic":
                # 获取用户动态
                try:
                    dynamics = await u.get_dynamics_new()
                except Exception:
                    dynamics = await u.get_dynamics()
                
                result = {
                    "type": "dynamic",
                    "data": [],
                    "has_more": dynamics.get("has_more", 0),
                    "raw": dynamics
                }
                
                # 处理新格式 items
                items = dynamics.get("items", [])
                if items:
                    for item in items:
                        dynamic_info = self._extract_new_dynamic_info(item)
                        result["data"].append(dynamic_info)
                else:
                    # 处理旧格式 cards
                    cards = dynamics.get("cards", [])
                    if cards:
                        for card in cards:
                            dynamic_info = self._extract_dynamic_info(card)
                            result["data"].append(dynamic_info)
                
                return json.dumps(result, ensure_ascii=False)
                
            elif action == "all_dynamics":
                # 获取所有动态
                all_dynamics = []
                offset = ""
                count = 0
                
                while count < limit:
                    try:
                        if offset:
                            dynamics = await u.get_dynamics_new(offset=offset)
                        else:
                            dynamics = await u.get_dynamics_new()
                    except Exception:
                        if offset:
                            dynamics = await u.get_dynamics(offset=offset)
                        else:
                            dynamics = await u.get_dynamics()
                    
                    # 处理新格式 items
                    items = dynamics.get("items", [])
                    if items:
                        for item in items:
                            if count >= limit:
                                break
                            dynamic_info = self._extract_new_dynamic_info(item)
                            all_dynamics.append(dynamic_info)
                            count += 1
                    else:
                        # 处理旧格式 cards
                        cards = dynamics.get("cards", [])
                        if not cards:
                            break
                        
                        for card in cards:
                            if count >= limit:
                                break
                            dynamic_info = self._extract_dynamic_info(card)
                            all_dynamics.append(dynamic_info)
                            count += 1
                    
                    has_more = dynamics.get("has_more", 0)
                    if not has_more:
                        break
                    
                    offset = dynamics.get("offset", "") or dynamics.get("next_offset", "")
                    if not offset:
                        break
                
                result = {
                    "type": "all_dynamics",
                    "total_count": len(all_dynamics),
                    "data": all_dynamics
                }
                
                return json.dumps(result, ensure_ascii=False)
                
            else:
                return json.dumps({"error": "不支持的操作类型"}, ensure_ascii=False)
                
        except ImportError:
            return json.dumps({"error": "需要安装 bilibili-api-python 库，请运行: pip install bilibili-api-python"}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": str(e)}, ensure_ascii=False)
    
    def _extract_new_dynamic_info(self, item: dict) -> dict:
        """从新格式的动态项中提取关键信息，包括完整的文本内容。"""
        dynamic_info = {
            "id": "",
            "type": "",
            "publish_time": 0,
            "content": "",
            "pictures": [],
            "video": {},
            "raw": item
        }
        
        try:
            # 提取基本信息
            dynamic_info["id"] = str(item.get("id_str", ""))
            dynamic_info["type"] = str(item.get("type", ""))
            
            modules = item.get("modules", {})
            
            # 提取发布时间
            if "module_author" in modules:
                module_author = modules.get("module_author", {})
                dynamic_info["publish_time"] = module_author.get("pub_ts", 0)
            
            # 提取内容
            content = ""
            if "module_dynamic" in modules:
                module_dynamic = modules.get("module_dynamic", {})
                
                # 尝试从 desc 中获取文本
                if "desc" in module_dynamic:
                    desc = module_dynamic.get("desc", {})
                    
                    # 直接的 text 字段
                    if "text" in desc:
                        content = desc.get("text", "")
                    
                    # rich_text 字段
                    if "rich_text" in desc:
                        rich_text = desc.get("rich_text", {})
                        if "text" in rich_text:
                            if not content:
                                content = rich_text.get("text", "")
                
                # 从 major 中提取
                if "major" in module_dynamic:
                    major = module_dynamic.get("major", {})
                    if major:
                        # 视频
                        if "archive" in major:
                            archive = major.get("archive", {})
                            dynamic_info["video"] = {
                                "bvid": archive.get("bvid", ""),
                                "aid": archive.get("aid", ""),
                                "title": archive.get("title", ""),
                                "desc": archive.get("desc", ""),
                                "cover": archive.get("cover", "")
                            }
                            if not content:
                                content = archive.get("desc", "")
                        
                        # 图文/文章
                        if "article" in major:
                            article = major.get("article", {})
                            if not content:
                                content = article.get("title", "")
                        
                        # 图片
                        if "draw" in major:
                            draw = major.get("draw", {})
                            if "items" in draw:
                                pics = draw.get("items", [])
                                for pic in pics:
                                    if "src" in pic:
                                        dynamic_info["pictures"].append(pic.get("src", ""))
            
            # 提取图片
            if "module_picture" in modules:
                module_picture = modules.get("module_picture", {})
                if "items" in module_picture:
                    pics = module_picture.get("items", [])
                    for pic in pics:
                        if "src" in pic:
                            dynamic_info["pictures"].append(pic.get("src", ""))
            
            dynamic_info["content"] = content
            
        except Exception:
            pass
        
        return dynamic_info
    
    def _extract_dynamic_info(self, card: dict) -> dict:
        """从旧格式的动态卡片中提取关键信息。"""
        dynamic_info = {
            "id": "",
            "type": "",
            "publish_time": 0,
            "content": "",
            "pictures": [],
            "video": {},
            "raw": card
        }
        
        try:
            # 尝试不同的方式提取动态信息
            if "desc" in card:
                desc = card.get("desc", {})
                dynamic_info["id"] = str(desc.get("dynamic_id", ""))
                dynamic_info["type"] = desc.get("type", "")
                dynamic_info["publish_time"] = desc.get("timestamp", 0)
            
            # 提取内容
            if "card" in card:
                try:
                    card_data = json.loads(card.get("card", "{}"))
                    
                    # 提取文本内容
                    if "item" in card_data:
                        item = card_data.get("item", {})
                        if "content" in item:
                            dynamic_info["content"] = item.get("content", "")
                        if "description" in item:
                            if not dynamic_info["content"]:
                                dynamic_info["content"] = item.get("description", "")
                    
                    # 提取图片
                    if "item" in card_data:
                        item = card_data.get("item", {})
                        if "pictures" in item:
                            pics = item.get("pictures", [])
                            for pic in pics:
                                if "img_src" in pic:
                                    dynamic_info["pictures"].append(pic.get("img_src", ""))
                    
                    # 提取视频信息
                    if "aid" in card_data:
                        dynamic_info["video"] = {
                            "aid": card_data.get("aid", ""),
                            "title": card_data.get("title", ""),
                            "desc": card_data.get("desc", ""),
                            "pic": card_data.get("pic", "")
                        }
                    
                    # 如果还有其他内容字段，也尝试提取
                    if "dynamic" in card_data and not dynamic_info["content"]:
                        dynamic_info["content"] = card_data.get("dynamic", "")
                        
                except json.JSONDecodeError:
                    pass
            
        except Exception:
            pass
        
        return dynamic_info
