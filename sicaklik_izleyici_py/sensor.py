import random
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class SensorNode(Node):

  def __init__(self):
    super().__init__('sensor_node')
    # /sicaklik konusuna Float32 tipinde yayın yapacak publisher tanımlıyoruz
    self.publisher_ = self.create_publisher(Float32, '/sicaklik', 10)

    # Her 1 saniyede bir publish_temperature fonksiyonunu çalıştıracak timer
    self.timer = self.create_timer(1.0, self.publish_temperature)
    self.get_logger().info('Sıcaklık Sensörü Düğümü Başlatıldı.')

  def publish_temperature(self):
    msg = Float32()
    # 20.0 ile 40.0 arasında rastgele bir sıcaklık değeri üretip virgülden sonra 2 basamağa yuvarlıyoruz
    msg.data = round(random.uniform(20.0, 40.0), 2)

    self.publisher_.publish(msg)
    self.get_logger().info(f'Yayınlanan Sıcaklık: {msg.data} °C')


def main(args=None):
  rclpy.init(args=args)
  node = SensorNode()

  try:
    rclpy.spin(node)
  except KeyboardInterrupt:
    pass
  finally:
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
  main()
