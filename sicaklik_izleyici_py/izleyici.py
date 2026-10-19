import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class IzleyiciNode(Node):

  def __init__(self):
    super().__init__('izleyici_node')

    # BONUS: Eşik değerini declare_parameter ile parametre yapıyoruz (Varsayılan: 30.0)
    self.declare_parameter('esik_sicaklik', 30.0)

    # /sicaklik konusuna abone (subscriber) oluyoruz
    self.subscription = self.create_subscription(
        Float32, '/sicaklik', self.listener_callback, 10
    )
    self.subscription  # unused variable warning önlemek için

    self.get_logger().info('Sıcaklık İzleyici Düğümü Başlatıldı.')

  def listener_callback(self, msg):
    # Güncel parametre değerini okuyoruz
    esik = (
        self.get_parameter('esik_sicaklik').get_parameter_value().double_value
    )
    sicaklik = msg.data

    # Ekrana normal sıcaklık bilgisini basıyoruz
    self.get_logger().info(
        f'Ölçülen Sıcaklık: {sicaklik:.2f} °C (Eşik: {esik:.2f} °C)'
    )

    # Sıcaklık eşik değerin üzerindeyse get_logger().warn() ile uyarı veriyoruz
    if sicaklik > esik:
      self.get_logger().warn(
          f'YÜKSEK SICAKLIK UYARISI! Sıcaklık ({sicaklik:.2f} °C) belirlenen'
          f' eşik değerini ({esik:.2f} °C) aştı!'
      )


def main(args=None):
  rclpy.init(args=args)
  node = IzleyiciNode()

  try:
    rclpy.spin(node)
  except KeyboardInterrupt:
    pass
  finally:
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
  main()
