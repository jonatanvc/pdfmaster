import asyncio
import tempfile
import time
from pathlib import Path

from loguru import logger


async def cleanup_temp_files_loop() -> None:
    """
    Background task to periodically clean up old temporary files created by the bot.
    This prevents disk space leaks from orphaned files after crashes.
    """
    temp_dir = Path(tempfile.gettempdir())
    
    while True:
        try:
            logger.debug("Running periodic temporary files cleanup...")
            now = time.time()
            deleted_count = 0
            
            # Scans temp directory
            if temp_dir.exists():
                for file_path in temp_dir.iterdir():
                    # We can target files starting with specific prefixes if needed,
                    # but for safety we only delete files that are clearly older than 6 hours.
                    if file_path.is_file() and (now - file_path.stat().st_mtime) > 6 * 3600:
                        try:
                            # Heuristic: delete files that look like they could belong to our bot
                            # like .pdf, .png, .txt or files without extension in temp folder
                            if file_path.suffix in [".pdf", ".png", ".txt", ""] or file_path.name.startswith("tmp"):
                                file_path.unlink()
                                deleted_count += 1
                        except Exception as e:
                            logger.warning(f"Could not delete temp file {file_path}: {e}")
            
            if deleted_count > 0:
                logger.info(f"Cleaned up {deleted_count} old temporary files.")
                
        except Exception as e:
            logger.exception(f"Error during temp file cleanup: {e}")
            
        # Run every 1 hour
        await asyncio.sleep(3600)
