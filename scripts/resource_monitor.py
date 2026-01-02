"""
Sistema de Monitoreo de Recursos para OmniMaestro
Monitorea CPU, RAM y disco en tiempo real para hardware limitado (i5-7300HQ + 8GB RAM)
"""

import psutil
import json
import time
from pathlib import Path
from typing import Dict, Tuple, Optional
from datetime import datetime


class ResourceMonitor:
    """Monitor de recursos del sistema con validación de seguridad"""
    
    def __init__(self, log_path: Optional[str] = None):
        """
        Inicializa el monitor de recursos
        
        Args:
            log_path: Ruta al archivo de log (default: .resource_log.json)
        """
        if log_path is None:
            log_path = Path(__file__).parent.parent / ".resource_log.json"
        
        self.log_path = Path(log_path)
        self.max_ram_gb = 6.5  # Máximo usable en sistema de 8GB
        self.max_cpu_percent = 80  # Límite seguro para i5-7300HQ
        self.logs = self._load_logs()
    
    def _load_logs(self) -> list:
        """Carga logs previos del archivo JSON"""
        if self.log_path.exists():
            try:
                with open(self.log_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []
    
    def _save_logs(self):
        """Guarda logs al archivo JSON"""
        try:
            with open(self.log_path, 'w', encoding='utf-8') as f:
                json.dump(self.logs[-100:], f, indent=2, ensure_ascii=False)  # Keep last 100 entries
        except IOError as e:
            print(f"⚠️  Error guardando logs: {e}")
    
    def get_current_status(self) -> Dict:
        """
        Obtiene el estado actual de recursos del sistema
        
        Returns:
            Dict con información de CPU, RAM y disco
        """
        # CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count(logical=False) or psutil.cpu_count()
        
        # RAM
        memory = psutil.virtual_memory()
        ram_used_gb = memory.used / (1024**3)
        ram_total_gb = memory.total / (1024**3)
        ram_percent = memory.percent
        
        # Disco (buscar disco D:\ en Windows o disco raíz en Linux)
        try:
            if psutil.WINDOWS:
                # Try D:\ first, fallback to C:\
                try:
                    disk = psutil.disk_usage('D:\\')
                    disk_path = "D:\\"
                except:
                    disk = psutil.disk_usage('C:\\')
                    disk_path = "C:\\"
            else:
                disk = psutil.disk_usage('/')
                disk_path = "/"
            
            disk_free_gb = disk.free / (1024**3)
            disk_total_gb = disk.total / (1024**3)
            disk_percent = disk.percent
        except Exception as e:
            print(f"⚠️  Error leyendo disco: {e}")
            disk_free_gb = disk_total_gb = disk_percent = 0
            disk_path = "unknown"
        
        return {
            'timestamp': datetime.now().isoformat(),
            'cpu': {
                'percent': cpu_percent,
                'count': cpu_count,
                'per_cpu': psutil.cpu_percent(percpu=True)
            },
            'ram': {
                'used_gb': round(ram_used_gb, 2),
                'total_gb': round(ram_total_gb, 2),
                'percent': ram_percent,
                'available_gb': round(memory.available / (1024**3), 2)
            },
            'disk': {
                'path': disk_path,
                'free_gb': round(disk_free_gb, 2),
                'total_gb': round(disk_total_gb, 2),
                'percent': disk_percent
            }
        }
    
    def print_status(self):
        """Imprime el estado actual del sistema de forma legible"""
        status = self.get_current_status()
        
        print("\n" + "="*60)
        print("📊 ESTADO DEL SISTEMA")
        print("="*60)
        
        # CPU
        cpu = status['cpu']
        cpu_emoji = "🔥" if cpu['percent'] > 80 else "⚡" if cpu['percent'] > 50 else "✅"
        print(f"\n{cpu_emoji} CPU:")
        print(f"   Uso: {cpu['percent']}%")
        print(f"   Núcleos: {cpu['count']}")
        
        # RAM
        ram = status['ram']
        ram_emoji = "🔥" if ram['percent'] > 85 else "⚠️ " if ram['percent'] > 70 else "✅"
        print(f"\n{ram_emoji} RAM:")
        print(f"   Usado: {ram['used_gb']} GB / {ram['total_gb']} GB ({ram['percent']}%)")
        print(f"   Disponible: {ram['available_gb']} GB")
        
        # Disco
        disk = status['disk']
        disk_emoji = "⚠️ " if disk['free_gb'] < 10 else "✅"
        print(f"\n{disk_emoji} DISCO ({disk['path']}):")
        print(f"   Libre: {disk['free_gb']} GB / {disk['total_gb']} GB")
        print(f"   Uso: {disk['percent']}%")
        
        print("\n" + "="*60 + "\n")
    
    def check_safety(self, task_name: str, expected_ram_mb: int = 0, 
                     expected_cpu_percent: int = 0) -> Tuple[bool, str]:
        """
        Verifica si es seguro ejecutar una tarea dado el estado actual
        
        Args:
            task_name: Nombre de la tarea a ejecutar
            expected_ram_mb: RAM adicional esperada en MB
            expected_cpu_percent: CPU adicional esperada en %
            
        Returns:
            Tuple (is_safe, message)
        """
        status = self.get_current_status()
        
        # Validar RAM
        ram_current_gb = status['ram']['used_gb']
        ram_after_gb = ram_current_gb + (expected_ram_mb / 1024)
        
        if ram_after_gb > self.max_ram_gb:
            return False, (f"⚠️  RAM insuficiente para '{task_name}':\n"
                          f"   Actual: {ram_current_gb:.1f} GB\n"
                          f"   Esperado: +{expected_ram_mb/1024:.1f} GB\n"
                          f"   Total: {ram_after_gb:.1f} GB (máx: {self.max_ram_gb} GB)\n"
                          f"   💡 Cierra aplicaciones y vuelve a intentar")
        
        # Validar CPU
        cpu_current = status['cpu']['percent']
        cpu_after = cpu_current + expected_cpu_percent
        
        if cpu_after > self.max_cpu_percent:
            return False, (f"⚠️  CPU sobrecargada para '{task_name}':\n"
                          f"   Actual: {cpu_current:.0f}%\n"
                          f"   Esperado: +{expected_cpu_percent}%\n"
                          f"   Total: {cpu_after:.0f}% (máx: {self.max_cpu_percent}%)\n"
                          f"   💡 Espera a que finalicen otras tareas")
        
        # Validar espacio en disco
        disk_free = status['disk']['free_gb']
        if disk_free < 5:
            return False, (f"⚠️  Espacio en disco insuficiente:\n"
                          f"   Disponible: {disk_free:.1f} GB\n"
                          f"   Mínimo recomendado: 5 GB\n"
                          f"   💡 Libera espacio antes de continuar")
        
        return True, f"✅ Sistema listo para ejecutar '{task_name}'"
    
    def log_task(self, task_name: str, before: Dict, after: Dict, 
                 success: bool = True, notes: str = ""):
        """
        Registra la ejecución de una tarea
        
        Args:
            task_name: Nombre de la tarea
            before: Estado antes de la tarea
            after: Estado después de la tarea
            success: Si la tarea fue exitosa
            notes: Notas adicionales
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'task': task_name,
            'success': success,
            'resources': {
                'ram_delta_gb': round(after['ram']['used_gb'] - before['ram']['used_gb'], 2),
                'cpu_before': before['cpu']['percent'],
                'cpu_after': after['cpu']['percent'],
                'disk_delta_gb': round(before['disk']['free_gb'] - after['disk']['free_gb'], 2)
            },
            'notes': notes
        }
        
        self.logs.append(log_entry)
        self._save_logs()
        
        # Imprimir resumen
        delta_ram = log_entry['resources']['ram_delta_gb']
        delta_disk = log_entry['resources']['disk_delta_gb']
        
        status_emoji = "✅" if success else "❌"
        print(f"\n{status_emoji} Tarea: {task_name}")
        if abs(delta_ram) > 0.01:
            print(f"   RAM: {delta_ram:+.2f} GB")
        if abs(delta_disk) > 0.01:
            print(f"   Disco: {delta_disk:+.2f} GB")
        if notes:
            print(f"   Notas: {notes}")
    
    def get_summary(self) -> Dict:
        """Obtiene un resumen de las tareas ejecutadas"""
        if not self.logs:
            return {'total_tasks': 0}
        
        successful = sum(1 for log in self.logs if log.get('success', False))
        failed = len(self.logs) - successful
        
        total_ram_delta = sum(log['resources'].get('ram_delta_gb', 0) for log in self.logs)
        total_disk_delta = sum(log['resources'].get('disk_delta_gb', 0) for log in self.logs)
        
        return {
            'total_tasks': len(self.logs),
            'successful': successful,
            'failed': failed,
            'total_ram_used_gb': round(total_ram_delta, 2),
            'total_disk_used_gb': round(total_disk_delta, 2),
            'latest_tasks': [log['task'] for log in self.logs[-5:]]
        }


def main():
    """Demo del monitor de recursos"""
    print("🔧 OmniMaestro - Monitor de Recursos")
    
    monitor = ResourceMonitor()
    monitor.print_status()
    
    # Ejemplo de validación
    safe, msg = monitor.check_safety("Instalación de dependencias", 
                                     expected_ram_mb=2000, 
                                     expected_cpu_percent=30)
    print(msg)
    
    # Mostrar resumen
    summary = monitor.get_summary()
    if summary['total_tasks'] > 0:
        print(f"\n📊 Resumen de tareas:")
        print(f"   Total: {summary['total_tasks']}")
        print(f"   Exitosas: {summary['successful']}")
        print(f"   Fallidas: {summary['failed']}")


if __name__ == "__main__":
    main()
